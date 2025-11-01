import asyncio
import base64
import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models.m_message import Message
from app.models.m_user import User
from app.schemas.s_message import MessageCreate, MessageOut
from app.services.messaging import rabbitmq
from app.utils.deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/send", response_model=MessageOut)
async def send_message(
    msg: MessageCreate,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    sender_result = await session.execute(select(User).where(User.username == username))
    sender = sender_result.scalar_one()

    new_msg = Message(
        sender_id=sender.id,
        receiver_id=msg.receiver_id,
        group_id=msg.group_id,
        channel_id=msg.channel_id,
        content=msg.content,
        file_base64=msg.file_base64,
        is_image=msg.is_image,
        self_destruct=msg.self_destruct,
    )

    session.add(new_msg)
    await session.commit()
    await session.refresh(new_msg)

    # Publish to RabbitMQ
    queue_name = (
        f"user_{msg.receiver_id}"
        if msg.receiver_id
        else (f"group_{msg.group_id}" if msg.group_id else f"channel_{msg.channel_id}")
    )
    await rabbitmq.publish(
        queue_name,
        json.dumps(
            {
                "id": new_msg.id,
                "sender_id": sender.id,
                "content": msg.content,
                "is_image": msg.is_image,
                "self_destruct": msg.self_destruct,
            }
        ),
    )

    if msg.self_destruct:
        asyncio.create_task(schedule_self_destruct(session, new_msg.id))

    return new_msg


@router.post("/send-file")
async def send_file(
    receiver_id: int,
    file: UploadFile = File(...),
    is_image: bool = False,
    self_destruct: bool = False,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    sender_result = await session.execute(select(User).where(User.username == username))
    sender = sender_result.scalar_one()

    content = await file.read()
    base64_str = base64.b64encode(content).decode("utf-8")

    new_msg = Message(
        sender_id=sender.id,
        receiver_id=receiver_id,
        file_base64=base64_str,
        is_image=is_image,
        self_destruct=self_destruct,
    )
    session.add(new_msg)
    await session.commit()
    await session.refresh(new_msg)

    queue_name = (
        f"user_{new_msg.receiver_id}"
        if new_msg.receiver_id
        else (
            f"group_{new_msg.group_id}"
            if new_msg.group_id
            else f"channel_{new_msg.channel_id}"
        )
    )

    await rabbitmq.publish(
        queue_name,
        json.dumps(
            {
                "id": new_msg.id,
                "sender_id": sender.id,
                "is_image": is_image,
                "file_base64": base64_str,
                "self_destruct": self_destruct,
            }
        ),
    )

    if self_destruct:
        asyncio.create_task(schedule_self_destruct(session, new_msg.id))

    return {"message": "File sent"}


async def schedule_self_destruct(session: AsyncSession, message_id: int):
    await asyncio.sleep(5)
    await session.execute(delete(Message).where(Message.id == message_id))
    await session.commit()
