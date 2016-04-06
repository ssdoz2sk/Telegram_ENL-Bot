import logging

import plugins

logger = logging.getLogger(__name__)
bot = plugins.tracking.bot

@bot.message_handler( commands = [ 'echo' ] )
def echo_message(message):
    logger.info( "{} - {}".format( message.chat.id, message.text ) )
    mes = ""
    if len(message.text.split( " " )) == 1 :
        pass
    else:
        mes = " ".join(message.text.split(" ")[1:])

    bot.reply_to(message, "Reply: {}".format( mes) )
