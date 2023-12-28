from telebot import TeleBot
from telebot.types import Message

from utils.tg_tools.base import authenticator


def help_reply(bot: TeleBot, message: Message):
    is_group, is_administrator = authenticator(bot, message)
    resp = "这里是查询机器人,"
    if not is_group:
        bot.reply_to(message, f"{resp}请将该bot拉入群组中使用 /help 查询功能")
        return

    if is_administrator:
        text = (
            f"{resp}你的身份是管理员,可用的操作如下:\n"
            "/add 添加用户\n"
            "/del 删除用户\n"
            "/list 显示全部用户和绑定关系\n"
            "/status 查询你的使用情况\n"
            "/binding 绑定用户关系\n"
            "/unbind 解除绑定用户关系\n"
            "/search 查询用户使用情况\n"
            "\n以上均为大饼目前只实现 /all 查询全部规则使用情况"
        )
        bot.reply_to(message, text)
        return
    else:
        text = (
            f"{resp}你的身份是普通成员,可用的操作如下:\n"
            "/status 查询你的使用情况\n"
            "/binding 绑定用户\n"
            "\n以上均为大饼目前只实现 /all 查询全部规则使用情况"
        )
        bot.reply_to(message, text)
        return
