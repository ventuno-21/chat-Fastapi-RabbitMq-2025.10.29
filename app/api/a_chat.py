from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.s_message import MessageCreate, MessageOut
from app.models.m_message import Message
from app.models.m_user import User
from app.utils.deps import get_current_user
from app.db import get_session
from app.services.messaging import rabbitmq
from sqlalchemy import select
import json

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

    return new_msg
