from enum import Enum
from typing import Type

import pydantic

from classiq_interface.generator.function_params import FunctionParams


class TwoDimensionalEntanlgerInputs(Enum):
    IN = "IN"


class TwoDimensionalEntanlgerOutputs(Enum):
    OUT = "OUT"


class TwoDimensionalEntangler(FunctionParams):
    """
    Creates a two dimensional cluster state with the specified number of qubits and schmidt rank
    (log of schmidt number). When the desired schmidt rank is too high, a rectangular grid with schmidt rank
    floor(sqrt(qubit_count))-1 is generated.
    """

    qubit_count: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits for the entangler."
    )
    schmidt_factor: pydantic.conint(ge=0) = pydantic.Field(
        default=0, description="The required schmidt factor (log of schmidt number)."
    )
    is_input_zero: bool = pydantic.Field(
        default=True,
        description="Boolean determining whether the entangler must "
        "act on state |0...0>.",
    )

    def create_io_enums(self):
        if not self.is_input_zero:
            self._input_names = TwoDimensionalEntanlgerInputs
            self._output_names = TwoDimensionalEntanlgerOutputs
