import telebot

import bot_command

from utils import task


task.parse_command_line_args()
t = task.Task()
bot = telebot.TeleBot(t.bot_token)
bot_command.register_handlers(bot)

bot.remove_webhook()
bot.infinity_polling()
