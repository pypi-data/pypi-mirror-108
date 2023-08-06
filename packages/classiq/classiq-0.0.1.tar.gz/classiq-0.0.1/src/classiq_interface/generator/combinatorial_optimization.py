from typing import List

import pydantic

from classiq_interface.generator import problem_name_mapping
from classiq_interface.generator.circuit_outline import Qubit
from classiq_interface.hybrid.encoding_type import EncodingType
from classiq_interface.hybrid.problem_input import ProblemInput


class CombinatorialOptimizationConstraint(pydantic.BaseModel):
    variables: pydantic.conlist(item_type=Qubit, min_items=1)
    truth_table: List[bool]

    @pydantic.validator("truth_table")
    def truth_table_validator(cls, truth_table):
        if not any(truth_table):
            raise ValueError("truth table must contain at least 1 true value")

        return truth_table

    @pydantic.root_validator(skip_on_failure=True)
    def combinations_length_validator(cls, values):
        variables, truth_table = values.get("variables"), values.get("truth_table")

        assert (
            variables is not None and truth_table is not None
        ), "These can not be none, as skip_on_failure is True."

        possible_combinations_count = 2 ** len(variables)
        if len(truth_table) != possible_combinations_count:
            raise ValueError(
                f"length of truth_table truth table must be {possible_combinations_count}"
            )

        return values


class CombinatorialOptimization(pydantic.BaseModel):
    variables_count: pydantic.PositiveInt
    constraints: List[CombinatorialOptimizationConstraint]


# TODO: Move to a different file
class CombinatorialOptimizationProperties(pydantic.BaseModel):
    problem: ProblemInput = pydantic.Field(
        default=..., description="Problem input data"
    )
    encoding_type: EncodingType = pydantic.Field(
        default=None, description="Various encoding types to the combinatorial problem."
    )

    @pydantic.validator("problem", pre=True)
    def check_problem(cls, problem):
        if isinstance(problem, dict) and problem.get("name") is None:
            return problem

        return problem_name_mapping.parse_problem_input(problem)

    @pydantic.validator("encoding_type", always=True)
    def check_encoding_type(cls, encoding_type, values):
        if encoding_type:
            return encoding_type
        problem = values.get("problem")
        if not problem:
            return encoding_type
        encoding_type = problem_name_mapping.ENCODING_TYPE_DEFAULT[type(problem)]
        return encoding_type
