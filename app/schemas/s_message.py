from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    receiver_id: Optional[int]
    group_id: Optional[int]
    channel_id: Optional[int]
    content: Optional[str]
    file_base64: Optional[str]
    is_image: Optional[bool] = False
    self_destruct: Optional[bool] = False


class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: Optional[int]
    group_id: Optional[int]
    channel_id: Optional[int]
    content: Optional[str]
    file_base64: Optional[str]
    is_image: bool
    self_destruct: bool
    created_at: datetime

    # class Config:
    #     orm_mode = True
