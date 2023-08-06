import enum
from typing import Union

import pydantic

from classiq_interface.generator.generation_metadata import GenerationMetadata


class GenerationStatus(str, enum.Enum):
    NONE = "none"
    SUCCESS = "success"
    UNSAT = "unsat"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    ERROR = "error"


class GeneratedCircuit(pydantic.BaseModel):
    qasm: str
    # TODO: We should change this interface.
    image: str
    metadata: GenerationMetadata


class GenerationResult(pydantic.BaseModel):
    status: GenerationStatus
    details: Union[GeneratedCircuit, str]
