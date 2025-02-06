Telegram @Itz_Your_4Bhi
Copyright ©️ 2025


from Player import Config
from pyrogram import enums
from pyrogram.types import Message


async def BhaiChara(message: Message):
    if message.from_user and message.from_user.id in Config.SUDOERS:
        return True
    else:
        return False


async def Teammates(message: Message):
    if message.from_user:
        user = await message.chat.get_member(message.from_user.id)
        if user.status in [
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR,
        ]:
            return True
        elif message.from_user.id in Config.SUDOERS:
            return True
    elif message.sender_chat:
        if message.sender_chat.id == message.chat.id:
            return True
    else:
        return False
