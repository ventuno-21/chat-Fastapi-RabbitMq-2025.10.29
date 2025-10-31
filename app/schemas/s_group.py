from pydantic import BaseModel
from typing import List, Optional


class GroupCreate(BaseModel):
    name: str
    image: Optional[str] = None
    user_ids: List[int]


class GroupOut(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    user_ids: List[int]

    # class Config:
    #     orm_mode = True
