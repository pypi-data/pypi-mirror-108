from enum import Enum

import pydantic

from classiq_interface.generator import function_params


class QftAdderInputs(Enum):
    IN = "IN"


QftAdderOutputs = function_params.DefaultOutputNames


class QFTConstAdder(function_params.FunctionParams):
    """
    QFT Const Adder circuit.
    """

    num_input_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of  input qubits on which the Adder acts."
    )
    num_addend: pydantic.conint(ge=0) = pydantic.Field(
        default=0, description="The constant number to add."
    )
    overflow_bits: bool = pydantic.Field(
        default=True,
        description="Whether to extend the register with an overflow bits.",
    )

    _input_names = pydantic.PrivateAttr(default=QftAdderInputs)
    _output_names = pydantic.PrivateAttr(default=QftAdderOutputs)
