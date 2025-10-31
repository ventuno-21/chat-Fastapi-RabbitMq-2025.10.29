from pydantic import BaseModel
from typing import List, Optional


class ChannelCreate(BaseModel):
    name: str
    image: Optional[str] = None
    user_ids: List[int]


class ChannelOut(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    user_ids: List[int]

    # class Config:
    #     orm_mode = True
