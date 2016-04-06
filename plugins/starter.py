import logging

import plugins

logger = logging.getLogger( __name__ )
bot = plugins.tracking.bot

@bot.message_handler( commands=['get_chat_id'])
def send_chat_id(message):
    bot.send_message( message.chat.id, message.chat.id, reply_to_message_id=message.message_id )

@bot.message_handler( commands = [ 'iamspartacus' ] )
def iamspartacus_message(message):
    global_admins = bot.get_config_option( 'admins' )
    chat_id = message.chat.id
    if not global_admins:
        bot.send_message( chat_id, 'Starter: Configuring first admin: {}'.format(chat_id), reply_to_message_id=message.message_id )
        initial_admin_list = [ message.chat.username ]
        bot.config['admins'] = initial_admin_list
        bot.config.save()
    else:
        bot.send_message( chat_id, 'No! I am Spartacus!', reply_to_message_id=message.message_id )
