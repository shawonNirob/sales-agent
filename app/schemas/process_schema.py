from pydantic import BaseModel
from typing import Union

class LLMAction(BaseModel):
    action: str
    content: Union[str, list[str]]



