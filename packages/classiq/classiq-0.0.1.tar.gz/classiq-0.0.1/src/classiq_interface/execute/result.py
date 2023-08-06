import enum
from typing import Union, Optional

import pydantic


class ExecutionStatus(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class VaRResult(pydantic.BaseModel):
    var: float = None
    alpha: float = None


class SimulationResults(pydantic.BaseModel):
    var_results: Optional[VaRResult] = None
    result: Optional[float] = None


class ExecutionResult(pydantic.BaseModel):
    status: ExecutionStatus
    details: Union[SimulationResults, str]
