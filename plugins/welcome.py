import logging

import plugins

logger = logging.getLogger(__name__)
bot = plugins.tracking.bot
config = plugins.tracking.config
start_list = config.get_by_path( ['start'] )

@bot.message_handler( content_types = ['new_chat_participant'] )
def new_chat_particpant_welcome( message ):
    welcome( message )

@bot.message_handler( commands=['start', 'welcome'])
def welcome( message ):
    logger.info( "welcome, id : {}".format( message.chat.username if message.chat.id > 0 else message.from_user.username) )
    chat_id = str( message.chat.id )
    if chat_id in start_list:
        bot.reply_to( message, start_list[ chat_id ]['text'] )
    else:
        bot.reply_to( message, """
/setkeyword 設定聊天關鍵字，BOT自動回應
/getkeyword 目前設定中的關鍵字
/delkeyword 刪除聊天關鍵字，請勿惡意新增或刪除
/roll 擲骰子
/set_start 設定鍵入 /start or /welcome 會顯現的文字( 限群組 )
群組關鍵字如需限定指定人修改，即只有指定 Username(s) 能修改，請私 @BlackCatKnight
並附上群組 /get_chat_id 及可修改人的 Username 列表
其餘關鍵字有：
今日運勢、明日運勢...
""" )

@bot.message_handler( commands = [ 'set_start' ] )
def set_start( message ):
    if message.chat.id > 0:
        bot.reply_to( message, "You can't set the /start in private" )
    else:
        chat_id = str( message.chat.id )
        if chat_id in start_list:
            if start_list[ chat_id ]['username']:
                if not message.chat.username in start_list[ chat_id ]['username']:
                    bot.send_message( message.chat.id, "Permission denied" )
                    return
        msg = bot.send_message( message.chat.id, "OK. Send me the text which the bot responds when someone uses /start or /welcome" )
        bot.register_next_step_handler( msg, process_set_start )
        
def process_set_start( message ):
    chat_id = str( message.chat.id )
    if chat_id in start_list:
        start_list[ chat_id ]['text'] = message.text
    else:
        start_list[ chat_id ] = { 'username' : [], 'text' : message.text }
    config.set_by_path( ['start'], self.start_list )
    config.save()
    config.load()
    start_list = self.bot.config.get_option( 'start' )
    bot.send_message( message.chat.id, 'Success!' )
