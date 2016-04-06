import logging, time
import plugins

logger = logging.getLogger( __name__ )
# logger.setLevel( 'DEBUG' )
bot = plugins.tracking.bot

@bot.message_handler( func=lambda message: True )
def reply( message ):
    localtime = time.localtime( time.time() )
    t_hour = localtime.tm_hour
    if message.chat.id < 0:
        logger.debug( "{} - {}\n{}".format ( message.chat.title, 
                                            message.from_user.username, 
                                            message.text ) )
    else:
        logger.debug( "{}\n{}".format ( message.from_user.username, 
                                        message.text ) )
                                            
    if message.text.find( '安安' ) > -1:
        bot.send_message( message.chat.id, "安安，你好，給虧嗎？幾歲？住哪？")
    if message.text.find( '早安' ) > -1:
        if not 11 > t_hour >= 3:
            bot.send_message( message.chat.id, "幾點了還早！！" )
    elif message.text.find( '午安' ) > -1:
        if 10 > t_hour:
            bot.send_message( message.chat.id, "還沒中午阿！！" )
        elif 18 > t_hour > 15:
            bot.send_message( message.chat.id, "現在都快晚上了！！" )
        elif t_hour >= 18:
            bot.send_message( message.chat.id, "現在都幾點了！！" )
    elif message.text.find( '晚安' ) > -1:
        if 6 > t_hour >= 3:
            bot.send_message( message.chat.id, "這麼晚了還沒睡！！" )
        elif 18 >= t_hour >= 6:
            bot.send_message( message.chat.id, "現在不是說晚安的時間吧！！" )
        elif 21 > t_hour > 18:
            bot.send_message( message.chat.id, "這麼早睡！！" )
        else:
            bot.send_message( message.chat.id, "晚安！！" )

