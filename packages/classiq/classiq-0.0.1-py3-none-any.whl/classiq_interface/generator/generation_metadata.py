from typing import Optional, List

import pydantic
from classiq_interface.hybrid import problem_input, encoding_type
from classiq_interface.generator import finance


class HybridMetadata(pydantic.BaseModel):
    problem: problem_input.ProblemInput
    encoding_type: encoding_type.EncodingType
    num_ancillas: Optional[pydantic.conint(ge=0)] = 0
    permutation: List[int]
    is_qaoa: bool = False


class FinanceMetadata(pydantic.BaseModel):
    finance_attribute: Optional[finance.Finance]


class GenerationMetadata(pydantic.BaseModel):
    hybrid: Optional[HybridMetadata]
    finance: Optional[FinanceMetadata]
