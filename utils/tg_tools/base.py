
from typing import List
from telebot import TeleBot
from telebot.types import Message, ChatMember

def authenticator(bot: TeleBot, msg: Message):
    """
    消息发送者的身份验证
    @ is_group: bool
    @ is_administrator: bool
    """
    is_group, is_administrator = False, False

    is_group = True if msg.chat.type == "group" else False
    is_administrator = (
        True
        if bot.get_chat_member(msg.chat.id, msg.from_user.id).status in ("administrator", "creator")
        else False
    )

    return is_group, is_administrator

def is_administrator(id: int, members: List[ChatMember]) -> bool:
    for member in members:
        if member.user.id == id:
            return True
    return False
