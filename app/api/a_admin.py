from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.models.m_channel import Channel, ChannelUser, channel_user
from app.models.m_group import Group, GroupUser, group_user
from app.models.m_message import Message
from app.models.m_user import User
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/promote/{user_id}")
async def promote_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    await session.commit()
    return {"message": f"User {user.username} promoted to admin"}


@router.delete("/group/{group_id}/remove/{user_id}")
async def remove_from_group(
    group_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    """
    Remove a user from a group.
    Only admins are allowed to perform this action.
    """

    # Fetch the group along with its users
    result = await session.execute(
        select(Group).where(Group.id == group_id).options(selectinload(Group.users))
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Check if the current admin is indeed an admin in this group
    admin_ids_in_group = [user.id for user in group.users if user.is_admin]
    if admin.id not in admin_ids_in_group:
        raise HTTPException(
            status_code=403, detail="You must be an admin of this group"
        )

    #  Check if the target user is a member of the group
    member_ids = [user.id for user in group.users]
    if user_id not in member_ids:
        raise HTTPException(status_code=404, detail="User not found in this group")

    #  Remove the user from the group
    await session.execute(
        delete(GroupUser).where(
            GroupUser.group_id == group_id, GroupUser.user_id == user_id
        )
    )
    await session.commit()

    return {"message": f"User {user_id} removed from group {group_id}"}


@router.delete("/channel/{channel_id}/remove/{user_id}")
async def remove_from_channel(
    channel_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    result = await session.execute(
        select(Channel)
        .where(Channel.id == channel_id)
        .options(selectinload(Channel.users))
    )
    channel = result.scalar_one_or_none()

    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # check if admin is a member of channel
    admin_ids_in_channel = [user.id for user in channel.users if user.is_admin]
    if admin.id not in admin_ids_in_channel:
        raise HTTPException(
            status_code=403, detail="You must be an admin of this channel"
        )

    # check if usser is a member of channel
    target_user_ids = [user.id for user in channel.users]
    if user_id not in target_user_ids:
        raise HTTPException(status_code=404, detail="User not found in this channel")

    # delete a user
    await session.execute(
        delete(ChannelUser).where(
            ChannelUser.channel_id == channel_id, ChannelUser.user_id == user_id
        )
    )
    await session.commit()

    return {"message": f"User {user_id} removed from channel {channel_id}"}


@router.delete("/message/{message_id}")
async def delete_message(
    message_id: int,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    await session.execute(delete(Message).where(Message.id == message_id))
    await session.commit()
    return {"message": "Message deleted"}
