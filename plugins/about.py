import logging

import plugins

logger = logging.getLogger( __name__ )
bot = plugins.tracking.bot

@bot.message_handler( commands=['about'])
def send_chat_id(message):
    bot.send_message( message.chat.id, "made by : @BlackCatKnight" )
    bot.send_message( message.chat.id, "GitHub: https://github.com/ssdoz2sk/Telegram_ENL-Bot " )
