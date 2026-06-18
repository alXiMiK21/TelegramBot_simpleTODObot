#!!! вот в таком стиле в проекте обозначены ошибки!!!
import telebot
import os
from dotenv import load_dotenv

from defs import timeNow

import commands as cmd

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

cmd.start(bot) #начальные команды, ставить в самом начале
cmd.myTODO(bot)
cmd.addTODO(bot)
cmd.deleteTODO(bot)
cmd.editTODO(bot)
cmd.statTODO(bot)
cmd.base(bot) #базовые команды, ставить в самом конце

if __name__ == "__main__":
    print(f"Bot start in {timeNow('t')}")
    bot.infinity_polling()