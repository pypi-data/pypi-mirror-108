import logging
from dataclasses import dataclass

from fseval.pipeline.estimator import Estimator, TaskedEstimatorConfig
from fseval.pipeline.resample import Resample, ResampleConfig
from omegaconf import MISSING

from .._pipeline import Pipeline

logger = logging.getLogger(__name__)


@dataclass
class RankAndValidateConfig:
    _target_: str = (
        "fseval.pipelines.rank_and_validate._components.BootstrappedRankAndValidate"
    )
    name: str = "rank-and-validate"
    resample: ResampleConfig = MISSING
    ranker: TaskedEstimatorConfig = MISSING
    validator: TaskedEstimatorConfig = MISSING
    n_bootstraps: int = MISSING
    all_features_to_select: str = MISSING


@dataclass
class RankAndValidatePipeline(Pipeline):
    """Instantiated version of `RankAndValidateConfig`: the actual pipeline
    implementation."""

    name: str = MISSING
    resample: Resample = MISSING
    ranker: Estimator = MISSING
    validator: Estimator = MISSING
    n_bootstraps: int = MISSING
    all_features_to_select: str = MISSING

    def _get_config(self):
        return {
            key: getattr(self, key)
            for key in RankAndValidatePipeline.__dataclass_fields__.keys()
        }
