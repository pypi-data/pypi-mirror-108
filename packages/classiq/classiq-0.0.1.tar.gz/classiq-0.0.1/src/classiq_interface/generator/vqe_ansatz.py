from typing import List, Optional, Dict, Any, Literal

import pydantic

from classiq_interface.generator import custom_ansatz
from classiq_interface.generator.combinatorial_optimization import (
    CombinatorialOptimizationProperties,
)
from classiq_interface.generator.function_params import FunctionParams
from classiq_interface.mixer import MixerType, MIXER_TYPES_DEFAULT
from classiq_interface.hybrid.encoding_type import EncodingType


class VQEAnsatz(FunctionParams):
    """
    Parametric circuit for an optimization VQE solver.
    """

    problem_properties: CombinatorialOptimizationProperties = pydantic.Field(
        description="Properties of the " "combinatorial optimization " "problem"
    )
    mixer_types: List[MixerType] = pydantic.Field(
        default_factory=list,
        description="Ordered list of mixers applied in the ansatz.",
    )

    # Setting use_mcmtvchain=False creates ansatz with anti-control gates, which are currently not supported by qasm.
    # See Jira issue CAD-99 (https://classiq.atlassian.net/browse/CAD-99)
    use_mcmtvchain: Literal[True] = pydantic.Field(
        default=True,
        description="Use MCMTVchain for multi controlled "
        "gates. Currently must be True.",
    )
    custom_ansatz_name: Optional[custom_ansatz.CustomAnsatzType] = pydantic.Field(
        default=None, description="A custom ansatz type"
    )
    custom_ansatz_args: Optional[Dict[str, Any]] = pydantic.Field(
        default=None, description="the arguments to the custom ansatz"
    )

    @pydantic.validator("mixer_types", always=True)
    def check_mixer_types(cls, mixer_types, values):
        if mixer_types is None:
            mixer_types = MIXER_TYPES_DEFAULT[type(values["problem"])]
        return mixer_types

    @pydantic.validator("use_mcmtvchain", always=True)
    def check_use_mcmtvchain(cls, use_mcmtvchain, values):
        if use_mcmtvchain is None:
            if values["encoding_type"] == EncodingType.SERIAL:
                return True
            else:  # == EncodingType.NODES
                return False
        return use_mcmtvchain

    @property
    def custom_ansatz_args_class(self):
        if self.custom_ansatz_name is None:
            return None
        return custom_ansatz.CUSTOM_ANSATZ_ARGS_MAPPING[self.custom_ansatz_name]
