from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models.m_channel import Channel, ChannelUser, channel_user
from app.models.m_group import Group, GroupUser, group_user
from app.models.m_message import Message
from app.models.m_user import User, UserBlock, user_block
from app.schemas.s_channel import ChannelCreate
from app.schemas.s_group import GroupCreate
from app.utils.deps import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/block/{user_id}")
async def block_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    blocker = await session.execute(select(User).where(User.username == username))
    blocker_id = blocker.scalar_one().id
    await session.execute(
        insert(UserBlock).values(blocker_id=blocker_id, blocked_id=user_id)
    )
    await session.commit()
    return {"message": "User blocked"}


@router.post("/leave/group/{group_id}")
async def leave_group(
    group_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    user = await session.execute(select(User).where(User.username == username))
    user_id = user.scalar_one().id
    await session.execute(
        delete(GroupUser).where(
            GroupUser.group_id == group_id, GroupUser.user_id == user_id
        )
    )
    await session.commit()
    return {"message": "Left group"}


@router.post("/leave/channel/{channel_id}")
async def leave_channel(
    channel_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    user = await session.execute(select(User).where(User.username == username))
    user_id = user.scalar_one().id
    await session.execute(
        delete(ChannelUser).where(
            ChannelUser.channel_id == channel_id, ChannelUser.user_id == user_id
        )
    )
    await session.commit()
    return {"message": "Left channel"}


@router.delete("/message/{message_id}")
async def delete_own_message(
    message_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    user = await session.execute(select(User).where(User.username == username))
    user_id = user.scalar_one().id
    msg = await session.execute(
        select(Message).where(Message.id == message_id, Message.sender_id == user_id)
    )
    if not msg.scalar():
        raise HTTPException(status_code=403, detail="Not your message")
    await session.execute(delete(Message).where(Message.id == message_id))
    await session.commit()
    return {"message": "Message deleted"}


@router.post("/block/{user_id}")
async def block_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    blocker = await session.execute(select(User).where(User.username == username))
    blocker_id = blocker.scalar_one().id
    await session.execute(
        insert(user_block).values(blocker_id=blocker_id, blocked_id=user_id)
    )
    await session.commit()
    return {"message": "User blocked"}


@router.post("/leave/group/{group_id}")
async def leave_group(
    group_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    user = await session.execute(select(User).where(User.username == username))
    user_id = user.scalar_one().id
    await session.execute(
        delete(group_user).where(
            group_user.c.group_id == group_id, group_user.c.user_id == user_id
        )
    )
    await session.commit()
    return {"message": "Left group"}


@router.post("/leave/channel/{channel_id}")
async def leave_channel(
    channel_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    user = await session.execute(select(User).where(User.username == username))
    user_id = user.scalar_one().id
    await session.execute(
        delete(channel_user).where(
            channel_user.c.channel_id == channel_id, channel_user.c.user_id == user_id
        )
    )
    await session.commit()
    return {"message": "Left channel"}


@router.delete("/message/{message_id}")
async def delete_own_message(
    message_id: int,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    user = await session.execute(select(User).where(User.username == username))
    user_id = user.scalar_one().id
    msg = await session.execute(
        select(Message).where(Message.id == message_id, Message.sender_id == user_id)
    )
    if not msg.scalar():
        raise HTTPException(status_code=403, detail="Not your message")
    await session.execute(delete(Message).where(Message.id == message_id))
    await session.commit()
    return {"message": "Message deleted"}


@router.post("/create-group")
async def create_group(
    data: GroupCreate,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    group = Group(name=data.name, image=data.image)
    session.add(group)
    await session.commit()
    await session.refresh(group)

    for uid in data.user_ids:
        await session.execute(insert(GroupUser).values(group_id=group.id, user_id=uid))
    await session.commit()
    return {"message": "Group created", "group_id": group.id}


@router.post("/create-channel")
async def create_channel(
    data: ChannelCreate,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_user),
):
    channel = Channel(name=data.name, image=data.image)
    session.add(channel)
    await session.commit()
    await session.refresh(channel)

    for uid in data.user_ids:
        await session.execute(
            insert(ChannelUser).values(channel_id=channel.id, user_id=uid)
        )
    await session.commit()
    return {"message": "Channel created", "channel_id": channel.id}
