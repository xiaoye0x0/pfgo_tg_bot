import telebot

from apps.help_reply import help_reply
from apps.all_status import view as all_status_view


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["help"])
    def to_help_reply(message):
        help_reply(bot, message)

    @bot.message_handler(commands=["all"])
    def search_all_status(message):
        """ "查询全部规则使用情况"""
        all_status_view.get_all_status(bot, message)


# @bot.message_handler(commands=["add"])
# def add_member(message):
#     """添加用户"""
#     pass


# @bot.message_handler(commands=["del"])
# def del_member(message):
#     """删除用户"""
#     pass


# @bot.message_handler(commands=["list"])
# def list_member(message):
#     """显示全部用户和绑定关系"""
#     pass


# @bot.message_handler(commands=["status"])
# def status(message):
#     """查询使用情况"""
#     pass


# @bot.message_handler(commands=["binding"])
# def binding(message):
#     """绑定用户关系"""
#     pass


# @bot.message_handler(commands=["unbind"])
# def unbind(message):
#     """解除绑定用户关系"""
#     pass


# @bot.message_handler(commands=["search"])
# def search(message):
#     """查询其他用户使用情况"""
#     pass


# @bot.message_handler(commands=["add1"])
# def add_info(message):
#     bot.reply_to(message, "请输入要添加的信息：")
#     bot.register_next_step_handler_by_chat_id(message.chat.id, process_reply)


# def process_reply(message):
#     reply = message.text

#     # 在这里进行根据回复信息进行判断和处理
#     if reply == "example":
#         bot.reply_to(message, "回复信息符合条件！")
#     else:
#         bot.reply_to(message, "回复信息不符合条件！")


# @bot.message_handler(func=lambda message: True, content_types=["text"])
# def echo_message(message):
#     """
#     Handle all other messages
#     """
#     bot.reply_to(message, message.text)
