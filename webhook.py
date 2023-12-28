#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import logging
import fastapi
import uvicorn
import telebot

import bot_command

from utils import task
from utils.log import Logmanager


task.parse_command_line_args()
logger = Logmanager.create_logger("Init")

now_task = task.Task()
bot = telebot.TeleBot(now_task.bot_token)
bot_command.register_handlers(bot)
app = fastapi.FastAPI(docs=None, redoc_url=None)


@app.post(f"/{now_task.bot_token}/")
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


bot.remove_webhook()
bot.set_webhook(
    url=f"https://{now_task.webhook_url}:{now_task.webhook_port}/{now_task.bot_token}/",
)


uvicorn.run(
    app,
    host=now_task.running_host,
    port=now_task.running_port,
)
