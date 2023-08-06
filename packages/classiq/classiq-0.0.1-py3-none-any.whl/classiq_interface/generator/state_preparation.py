from enum import Enum
from typing import Tuple, Optional, Dict, Union, ClassVar

import pydantic

from classiq_interface.generator.function_params import FunctionParams
from classiq_interface.generator.preferences.optimization import (
    StatePrepOptimizationMethod,
)
from classiq_interface.generator.range_types import NonNegativeFloatRange


class Metrics(str, Enum):
    KL = "KL"
    L2 = "L2"
    L1 = "L1"
    MAX_PROBABILITY = "MAX_PROBABILITY"


class PMF(pydantic.BaseModel):
    pmf: Tuple[pydantic.confloat(ge=0, le=1), ...]

    @pydantic.validator("pmf")
    def pmf_validator(cls, pmf):
        n = len(pmf)
        is_power_of_two = (n != 0) and (n & (n - 1) == 0)
        if not is_power_of_two:
            raise ValueError("Probabilities length must be power of 2")

        if round(sum(pmf), 8) != 1:
            raise ValueError("Probabilities do not sum to 1")

        return pmf


class GaussianMoments(pydantic.BaseModel):
    mu: float
    sigma: pydantic.confloat(gt=0)


class GaussianMixture(pydantic.BaseModel):
    gaussian_moment_list: Tuple[GaussianMoments, ...]


class StatePreparation(FunctionParams):
    probabilities: Union[PMF, GaussianMixture]
    depth_range: Optional[NonNegativeFloatRange] = NonNegativeFloatRange(
        lower_bound=0, upper_bound=float("inf")
    )
    cnot_count_range: Optional[NonNegativeFloatRange] = NonNegativeFloatRange(
        lower_bound=0, upper_bound=float("inf")
    )
    error_metric: Optional[Dict[Metrics, NonNegativeFloatRange]] = pydantic.Field(
        default_factory=lambda: {
            Metrics.KL: NonNegativeFloatRange(lower_bound=0, upper_bound=float("inf"))
        }
    )
    optimization_method: Optional[
        StatePrepOptimizationMethod
    ] = StatePrepOptimizationMethod.KL
    num_qubits: Optional[int] = None

    class Config:
        extra = "forbid"
