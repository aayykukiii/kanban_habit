from pydantic import BaseModel, ConfigDict
from typing import Optional



class TagCreate(BaseModel):
    name: str
    color: str


class TagRead(BaseModel):
    id: int
    name: str
    color: str

    model_config = ConfigDict(from_attributes=True)


class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None