import logging
from random import randint

import plugins

logger = logging.getLogger(__name__)
bot = plugins.tracking.bot

@bot.message_handler( commands=['roll'])
def roll( message ):
    dice1 = randint(1,6)
    dice2 = randint(1,6)
    dice3 = randint(1,6)
    bot.reply_to(message, "擲出 {}點, {}點, {}點，共 {} 點".format( dice1, dice2, dice3, dice1+dice2+dice3) )
