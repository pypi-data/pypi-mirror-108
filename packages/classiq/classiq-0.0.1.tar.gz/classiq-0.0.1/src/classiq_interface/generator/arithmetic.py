import pydantic
from typing import Union, Optional
from classiq_interface.generator.function_params import FunctionParams
from enum import Enum


DEFAULT_RIGHT_ARG_NAME = "right_arg"
DEFAULT_LEFT_ARG_NAME = "left_arg"
DEFAULT_OUT_NAME = "out"


class RegisterUserInput(pydantic.BaseModel):
    size: pydantic.PositiveInt
    name: Optional[str] = None


class BinaryOpWithIntInputs(FunctionParams):
    left_arg: Union[pydantic.conint(ge=0), RegisterUserInput]
    right_arg: Union[pydantic.conint(ge=0), RegisterUserInput]
    output_size: Optional[pydantic.PositiveInt]
    output_name: Optional[str]

    @pydantic.root_validator()
    def validate_right_arg(
        cls, values
    ) -> Union[pydantic.conint(ge=0), RegisterUserInput]:
        if isinstance(values.get("left_arg"), int) and isinstance(
            values.get("right_arg"), int
        ):
            raise ValueError("One argument must be a register")
        return values

    def create_io_enums(self):
        output_name = self.output_name if self.output_name else DEFAULT_OUT_NAME
        self._output_names = Enum("BinaryOpOutputs", {output_name: output_name})

        if isinstance(self.left_arg, RegisterUserInput) and isinstance(
            self.right_arg, RegisterUserInput
        ):
            left_arg_name = (
                self.left_arg.name if self.left_arg.name else DEFAULT_LEFT_ARG_NAME
            )
            right_arg_name = (
                self.right_arg.name if self.right_arg.name else DEFAULT_RIGHT_ARG_NAME
            )
            self._input_names = Enum(
                "BinaryOpInputs",
                {left_arg_name: left_arg_name, right_arg_name: right_arg_name},
            )
            return

        if isinstance(self.left_arg, RegisterUserInput):
            arg_name = (
                self.left_arg.name if self.left_arg.name else DEFAULT_LEFT_ARG_NAME
            )
        else:
            assert isinstance(
                self.right_arg, RegisterUserInput
            ), "At least one argument should be a register"
            arg_name = (
                self.right_arg.name if self.right_arg.name else DEFAULT_RIGHT_ARG_NAME
            )

        self._input_names = Enum("BinaryOpInputs", {arg_name: arg_name})


class BitwiseAnd(BinaryOpWithIntInputs):
    pass
