from typing import Optional

import pydantic

from classiq_interface.generator.generation_metadata import GenerationMetadata


class AmplitudeEstimation(pydantic.BaseModel):
    alpha: float = pydantic.Field(
        default=0.05, desctiption="Confidence level of the AE algorithm"
    )
    epsilon: float = pydantic.Field(
        default=0.01, desctiption="precision for estimation target `a`"
    )
    binary_search_threshold: Optional[pydantic.confloat(ge=0, le=1)] = pydantic.Field(
        description="The required probability on the tail of the distribution (1 - percentile)"
    )


class GeneralPreferences(pydantic.BaseModel):
    simulator: str = "qasm_simulator"
    num_shots: int = 100
    amplitude_estimation: Optional[AmplitudeEstimation] = None


class ExecuteProblem(pydantic.BaseModel):
    problem_preferences: GeneralPreferences = pydantic.Field(
        default_factory=GeneralPreferences, description="preferences for the execution"
    )

    problem_data: GenerationMetadata = pydantic.Field(
        default=None, description="Data returned from the generation procedure."
    )
