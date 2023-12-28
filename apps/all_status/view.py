from telebot import TeleBot
from telebot.types import Message
from utils.base import str_in_list_str

from utils.pfgo_spider.spider import PfgoSpider
from utils.task import Task
from utils.tg_tools.base import is_administrator


def get_all_status(bot: TeleBot, message: Message):
    chat_id = message.chat.id
    task = Task()
    bot_info = bot.get_me()
    if is_administrator(bot_info.id, bot.get_chat_administrators(chat_id)):
        sent_message = bot.send_message(chat_id, "开始查询数据")
        s = PfgoSpider(task.pfgo_url, task.username, task.password)
        try:
            data = s.get_forward_rules()
            result_text = ""
            for _, v in data.items():
                if str_in_list_str(v["name"], task.hide):
                    continue
                result_text += "规则'{}'已使用: {}GB\n".format(v["name"], v["traffic"])
            bot.edit_message_text(result_text, chat_id, sent_message.message_id)
        except:
            bot.edit_message_text("查询失败", chat_id, sent_message.message_id)
    else:
        sent_message = bot.send_message(chat_id, "未检测到本Bot的创建者是管理员,结束查询")
