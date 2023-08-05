import os
from typing import List, Union
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
import warnings
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from mikeio import Dfs0, Dfsu, Dataset, eum
from .observation import Observation, PointObservation, TrackObservation
from .comparison import PointComparer, TrackComparer, ComparerCollection, BaseComparer
from .plot import plot_observation_positions
from .utils import make_unique_index


class ModelResultInterface(ABC):
    @abstractmethod
    def add_observation(self, observation, item, weight, validate_eum):
        pass

    @abstractmethod
    def extract(self) -> ComparerCollection:
        pass

    @abstractmethod
    def plot_observation_positions(self, figsize):
        pass


class ModelResult(ModelResultInterface):
    """
    The result from a MIKE FM simulation (either dfsu or dfs0)

    Examples
    --------
    >>> mr = ModelResult("Oresund2D.dfsu")

    >>> mr = ModelResult("Oresund2D_points.dfs0", name="Oresund")
    """

    def __init__(self, filename: str, name: str = None):
        # TODO: add "start" as user may wish to disregard start from comparison
        self.filename = filename
        ext = os.path.splitext(filename)[-1]
        if ext == ".dfsu":
            self.dfs = Dfsu(filename)
        # elif ext == '.dfs2':
        #    self.dfs = Dfs2(filename)
        elif ext == ".dfs0":
            self.dfs = Dfs0(filename)
        else:
            raise ValueError(f"Filename extension {ext} not supported (dfsu, dfs0)")

        self.observations = {}

        if name is None:
            name = os.path.basename(filename).split(".")[0]
        self.name = name

    def __repr__(self):
        out = []
        out.append("<fmskill.ModelResult>")
        out.append(self.filename)
        return "\n".join(out)

    @staticmethod
    def from_config(configuration: Union[dict, str], validate_eum=True):

        if isinstance(configuration, str):
            with open(configuration) as f:
                contents = f.read()
            configuration = yaml.load(contents, Loader=yaml.FullLoader)

        mr = ModelResult(
            filename=configuration["filename"], name=configuration.get("name")
        )
        for connection in configuration["observations"]:
            observation = connection["observation"]

            if observation.get("type") == "track":
                obs = TrackObservation(**observation)
            else:
                obs = PointObservation(**observation)

            mr.add_observation(obs, item=connection["item"], validate_eum=validate_eum)

        return mr

    def to_config(self, filename: Union[str, Path]):
        """
        Parameters
        ----------
        filename: str or Path
            Save configuration in yaml format

        Notes
        -----
        1. Manually create your skill assessment in fmskill as usual
        2. When you are satisfied, save config: cc.to_config('conf.yml') or similar
        3. Later: run your reporting from the commandline e.g. directly after model execution
        """
        raise NotImplementedError()

    def add_observation(self, observation, item=None, weight=1.0, validate_eum=True):
        """Add an observation to this ModelResult

        Parameters
        ----------
        observation : <fmskill.Observation>
            Observation object for later comparison
        item : (str, integer), optional
            Model item name or number corresponding to the observation
            If None, then try to infer from observation eum value.
            Default: None
        weight: float, optional
            Relative weight used in weighted skill calculation, default 1.0
        validate_eum: bool, optional
            Require eum type and units to match between model and observation?
            Defaut: True
        """
        if item is None:
            item = self._infer_model_item(observation)

        ok = self._validate_observation(observation)
        if ok and validate_eum:
            ok = self._validate_item_eum(observation, item)
            if not ok:
                raise ValueError(
                    "Could not add observation, to ignore EUM validation, try validate_eum=False"
                )
        if ok:
            observation.model_item = item
            observation.weight = weight
            self.observations[observation.name] = observation
        else:
            warnings.warn("Could not add observation")

        return self

    def _validate_observation(self, observation) -> bool:
        ok = False
        if self.is_dfsu:
            if isinstance(observation, PointObservation):
                ok = self.dfs.contains([observation.x, observation.y])
                if not ok:
                    raise ValueError("Observation outside domain")
            elif isinstance(observation, TrackObservation):
                ok = True
        elif self.is_dfs0:
            # TODO: add check on name
            ok = True
        if ok:
            ok = self._validate_start_end(observation)
            if not ok:
                warnings.warn("No time overlap between model result and observation!")
        return ok

    def _validate_start_end(self, observation: Observation) -> bool:
        try:
            # need to put this in try-catch due to error in dfs0 in mikeio
            if observation.end_time < self.dfs.start_time:
                return False
            if observation.start_time > self.dfs.end_time:
                return False
        except:
            pass
        return True

    def _validate_item_eum(
        self, observation: Observation, item, mod_items=None
    ) -> bool:
        """Check that observation and model item eum match"""
        if mod_items is None:
            mod_items = self.dfs.items
        ok = True
        obs_item = observation.itemInfo
        if obs_item.type == eum.EUMType.Undefined:
            warnings.warn(f"{observation.name}: Cannot validate as type is Undefined.")
            return ok

        item = self._get_model_item(item, mod_items)
        if item.type != obs_item.type:
            ok = False
            warnings.warn(
                f"{observation.name}: Item type should match. Model item: {item.type.display_name}, obs item: {obs_item.type.display_name}"
            )
        if item.unit != obs_item.unit:
            ok = False
            warnings.warn(
                f"{observation.name}: Unit should match. Model unit: {item.unit.display_name}, obs unit: {obs_item.unit.display_name}"
            )
        return ok

    def _get_model_item(self, item, mod_items=None) -> eum.ItemInfo:
        """Given str or int find corresponding model itemInfo"""
        if mod_items is None:
            mod_items = self.dfs.items
        n_items = len(mod_items)
        if isinstance(item, int):
            if (item < 0) or (item >= n_items):
                raise ValueError(f"item number must be between 0 and {n_items}")
        elif isinstance(item, str):
            item_names = [i.name for i in mod_items]
            try:
                item = item_names.index(item)
            except ValueError:
                raise ValueError(f"item not found in model items ({item_names})")
        else:
            raise ValueError("item must be an integer or a string")
        return mod_items[item]

    def _infer_model_item(
        self,
        observation: Observation,
        mod_items: List[eum.ItemInfo] = None,
    ) -> int:
        """Attempt to infer model item by matching observation eum with model eum"""
        if mod_items is None:
            mod_items = self.dfs.items

        if len(mod_items) == 1:
            # accept even if eum does not match
            return 0

        mod_items = [(x.type, x.unit) for x in mod_items]
        obs_item = (observation.itemInfo.type, observation.itemInfo.unit)

        pot_items = [j for j, mod_item in enumerate(mod_items) if mod_item == obs_item]

        if len(pot_items) == 0:
            raise Exception("Could not infer")
        if len(pot_items) > 1:
            raise ValueError(
                f"Multiple matching model items found! (Matches {pot_items})."
            )

        return pot_items[0]

    def extract(self) -> ComparerCollection:
        """Extract model result in all observations"""
        cc = ComparerCollection()
        for obs in self.observations.values():
            comparer = self.extract_observation(obs, obs.model_item, validate=False)
            if comparer is not None:
                cc.add_comparer(comparer)
        return cc

    def extract_observation(
        self,
        observation: Union[PointObservation, TrackObservation],
        item: Union[int, str] = None,
        validate: bool = True,
    ) -> BaseComparer:
        """Compare this ModelResult with an observation

        Parameters
        ----------
        observation : <PointObservation> or <TrackObservation>
            Observation to be compared
        item : str, integer
            ModelResult item name or number
            If None, then try to infer from observation eum value.
            Default: None
        validate: bool, optional
            Validate if observation is inside domain and that eum type
            and units; Defaut: True

        Returns
        -------
        <fmskill.BaseComparer>
            A comparer object for further analysis or plotting
        """
        if item is None:
            item = self._infer_model_item(observation)

        if validate:
            ok = self._validate_observation(observation)
            if ok:
                ok = self._validate_item_eum(observation, item)
            if not ok:
                raise ValueError("Could not extract observation")

        if isinstance(observation, PointObservation):
            df_model = self._extract_point(observation, item)
            comparer = PointComparer(observation, df_model)
        elif isinstance(observation, TrackObservation):
            df_model = self._extract_track(observation, item)
            comparer = TrackComparer(observation, df_model)
        else:
            raise ValueError("Only point and track observation are supported!")

        if len(comparer.df) == 0:
            warnings.warn(f"No overlapping data in found for {observation.name}!")
            comparer = None

        return comparer

    def _extract_point(self, observation: PointObservation, item) -> pd.DataFrame:
        ds_model = None
        if self.is_dfsu:
            ds_model = self._extract_point_dfsu(observation.x, observation.y, item)
        elif self.is_dfs0:
            ds_model = self._extract_point_dfs0(item)

        return ds_model.to_dataframe()

    def _extract_point_dfsu(self, x, y, item) -> Dataset:
        xy = np.atleast_2d([x, y])
        elemids, _ = self.dfs.get_2d_interpolant(xy, n_nearest=1)
        ds_model = self.dfs.read(elements=elemids, items=[item])
        ds_model.items[0].name = self.name
        return ds_model

    def _extract_point_dfs0(self, item) -> Dataset:
        ds_model = self.dfs.read(items=[item])
        ds_model.items[0].name = self.name
        return ds_model

    def _extract_track(self, observation: TrackObservation, item) -> pd.DataFrame:
        df = None
        if self.is_dfsu:
            ds_model = self._extract_track_dfsu(observation, item)
            df = ds_model.to_dataframe().dropna()
        elif self.is_dfs0:
            ds_model = self.dfs.read(items=[0, 1, item])
            ds_model.items[-1].name = self.name
            df = ds_model.to_dataframe().dropna()
            df.index = make_unique_index(df.index, offset_in_seconds=0.01)
        return df

    def _extract_track_dfsu(self, observation: TrackObservation, item) -> Dataset:
        ds_model = self.dfs.extract_track(track=observation.df, items=[item])
        ds_model.items[-1].name = self.name
        return ds_model

    def plot_observation_positions(self, figsize=None):
        """Plot observation points on a map showing the model domain

        Parameters
        ----------
        figsize : (float, float), optional
            figure size, by default None
        """
        if self.is_dfs0:
            warnings.warn(
                "Plotting observations is only supported for dfsu ModelResults"
            )
            return

        ax = plot_observation_positions(
            dfs=self.dfs, observations=self.observations.values()
        )

        return ax

    def plot_temporal_coverage(self, limit_to_model_period=True):

        fig, ax = plt.subplots()
        y = np.repeat(0.0, 2)
        x = self.dfs.start_time, self.dfs.end_time
        plt.plot(x, y)
        labels = ["Model"]

        plt.plot([self.dfs.start_time, self.dfs.end_time], y)
        for key, obs in self.observations.items():
            y += 1.0
            plt.plot(obs.time, y[0] * np.ones_like(obs.values), "_", markersize=5)
            labels.append(key)
        if limit_to_model_period:
            plt.xlim([self.dfs.start_time, self.dfs.end_time])

        plt.yticks(np.arange(0, len(self.observations) + 1), labels)
        fig.autofmt_xdate()
        return ax

    @property
    def is_dfsu(self):
        return isinstance(self.dfs, Dfsu)

    @property
    def is_dfs0(self):
        return isinstance(self.dfs, Dfs0)


class ModelResultCollection(ModelResultInterface):
    """
    A collection of results from multiple MIKE FM simulations
    with the same "topology", e.g. several "runs" of the same model.

    Examples
    --------
    >>> mr1 = ModelResult("HKZN_local_2017_v1.dfsu", name="HKZN_v1")
    >>> mr2 = ModelResult("HKZN_local_2017_v2.dfsu", name="HKZN_v2")
    >>> mr = ModelResultCollection([mr1, mr2])
    """

    _mr0 = None

    @property
    def names(self):
        return list(self.modelresults.keys())

    @property
    def observations(self):
        return self._mr0.observations

    # has_same_topology = False

    def __init__(self, modelresults=None):
        self.modelresults = {}
        if modelresults is not None:
            for mr in modelresults:
                self.add_modelresult(mr)
        self._mr0 = self.modelresults[self.names[0]]

    def __repr__(self):
        out = []
        out.append(f"<{type(self).__name__}>")
        for key, value in self.modelresults.items():
            out.append(f"{type(value).__name__}: {key}")
        return str.join("\n", out)

    def __getitem__(self, x):
        return self.modelresults[x]

    def add_modelresult(self, modelresult):
        assert isinstance(modelresult, ModelResult)
        self.modelresults[modelresult.name] = modelresult

    def add_observation(self, observation, item=None, weight=1.0, validate_eum=True):
        """Add an observation to all ModelResults in collection

        Parameters
        ----------
        observation : <fmskill.PointObservation>
            Observation object for later comparison
        item : (str, integer), optional
            ModelResult item name or number corresponding to the observation
            If None, then try to infer from observation eum value.
            Default: None
        weight: float, optional
            Relative weight used in weighted skill calculation, default 1.0
        validate_eum: bool, optional
            Require eum type and units to match between model and observation?
            Defaut: True
        """
        for mr in self.modelresults.values():
            mr.add_observation(observation, item, weight, validate_eum)

    def extract_observation(
        self,
        observation: Union[PointComparer, TrackComparer],
        item: Union[int, str] = None,
        validate: bool = True,
    ) -> BaseComparer:
        """Compare all ModelResults in collection with an observation

        Parameters
        ----------
        observation : <PointObservation> or <TrackObservation>
            Observation to be compared
        item : str, integer
            ModelResult item name or number
            If None, then try to infer from observation eum value.
            Default: None
        validate: bool, optional
            Validate if observation is inside domain and that eum type
            and units match; Defaut: False

        Returns
        -------
        <fmskill.BaseComparer>
            A comparer object for further analysis or plotting
        """
        if item is None:
            for mr in self.modelresults.values():
                itemj = mr._infer_model_item(observation)
                if item is None:
                    item = itemj
                if item != itemj:
                    raise Exception(
                        "Cannot infer model item as different ModelResults in collection give different match"
                    )

        if validate:
            ok = True
            for mr in self.modelresults.values():
                if ok:
                    ok = mr._validate_observation(observation)
                if ok:
                    ok = mr._validate_item_eum(observation, item)
                if not ok:
                    raise ValueError("Could not extract observation")

        if isinstance(observation, PointObservation):
            comparer = self._compare_point_observation(observation, item)
        elif isinstance(observation, TrackObservation):
            comparer = self._compare_track_observation(observation, item)
        else:
            raise ValueError("Only point and track observation are supported!")

        return comparer

    def _compare_point_observation(self, observation, item) -> PointComparer:
        """Compare all ModelResults in collection with a point observation

        Parameters
        ----------
        observation : <fmskill.PointObservation>
            Observation to be compared
        item : str, integer
            ModelResult item name or number

        Returns
        -------
        <fmskill.PointComparer>
            A comparer object for further analysis or plotting
        """
        assert isinstance(observation, PointObservation)
        df_model = []
        for mr in self.modelresults.values():
            df_model.append(mr._extract_point(observation, item))

        return PointComparer(observation, df_model)

    def _compare_track_observation(self, observation, item) -> TrackComparer:
        """Compare all ModelResults in collection with a track observation

        Parameters
        ----------
        observation : <fmskill.TrackObservation>
            Observation to be compared
        item : str, integer
            ModelResult item name or number

        Returns
        -------
        <fmskill.TrackComparer>
            A comparer object for further analysis or plotting
        """
        assert isinstance(observation, TrackObservation)
        df_model = []
        for mr in self.modelresults.values():
            assert isinstance(mr, ModelResult)
            df_model.append(mr._extract_track(observation, item))

        return TrackComparer(observation, df_model)

    def extract(self) -> ComparerCollection:
        """extract model result in all observations"""
        cc = ComparerCollection()

        for obs in self.observations.values():
            comparer = self.extract_observation(obs, obs.model_item)
            if comparer is not None:
                cc.add_comparer(comparer)
        return cc

    def plot_observation_positions(self, figsize=None):
        """Plot observation points on a map showing the first model domain

        Parameters
        ----------
        figsize : (float, float), optional
            figure size, by default None
        """
        return self._mr0.plot_observation_positions(figsize=figsize)
