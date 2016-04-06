import logging, sys, re, random
import plugins

logger = logging.getLogger(__name__)
bot = plugins.tracking.bot
config = plugins.tracking.config
autorepliers_list = config.get_by_path( ['autoreply'] )

@bot.message_handler( commands = [ 'getkeyword' ] )
def getkeyword( message ):
    msg = ''
    for reply_list in autorepliers_list:
        msg += 'Keyword:\n    {}\nReply:\n    {}\nPriority: {}\n{}\n'.format( ',\n    '.join( reply_list['keyword'] ),
                                                                              ',\n    '.join( reply_list['reply'] ),
                                                                              reply_list['priority'],
                                                                              '=' * 16 )
        if len( msg ) > 750:
            bot.send_message( message.chat.id, msg )
            msg = ''
    bot.send_message( message.chat.id, msg )

@bot.message_handler( commands = [ 'delkeyword' ] )
def delkeyword( message ):
    if message.chat.id < 0 :
        bot.reply_to( message, "Please speak to BOT 1 to 1 ")
        return
        
    text = 'Select the one you want to delete.\n-1: Canel \n' + '=' * 16 + '\n'
    for index, reply_list in zip( range( len( autorepliers_list ) ), autorepliers_list ):
        text += '{}:\n--Keyword:\n      {}\n--Reply:\n      {}\n--Priority: {}\n{}\n'.format( 
                          index,
                          ',\n      '.join( reply_list['keyword'] ),
                          ',\n      '.join( reply_list['reply'] ),
                          reply_list['priority'],
                          '=' * 16 )
        if len( text ) > 750:
            msg = bot.send_message( message.chat.id, text )
            text = ''
    msg = msg if len( text ) == 0 else bot.send_message( message.chat.id, text )
    bot.register_next_step_handler( msg, process_del_keyword )
    
    
@bot.message_handler( commands = [ 'setkeyword' ] )
def help_message( message ):
    if message.chat.id < 0 :
        bot.reply_to( message, "Please speak to BOT 1 to 1 ")
        return
    msg = bot.reply_to( message, """
OK. Send me a list of keyword for your bot. Please use this format:
priority: 1 - 100 ( option )

keyword:
Hello
Hi

reply:
Hello moto

======================
If someone say 'hello' or 'hi', the bot will reply Hello moto.
If the reply list is not only 'one' line, the bot will reply one line in reply list random.
""")
    bot.register_next_step_handler( msg, process_set_keyword )
    
    
@bot.message_handler( func = lambda message : True )
def send_reply( message ):
    if autorepliers_list:
        find = False
        for pair in autorepliers_list:
            for kw in pair['keyword']:
                if _words_in_text( kw, message.text ):
                    bot.send_message( message.chat.id, random.choice( pair['reply'] ) )
                    find = True
                    break
            if find:
                break
                
def process_set_keyword( message ):
    try:
        message_list = [ each_line.strip() for each_line in message.text.splitlines() if each_line != ''  ]
        
        priority_string = re.split( ': ',message_list[0] )
        priority = 50
        if priority_string[0] == 'priority':
            priority = int( priority_string[1] )
            if priority <= 0 or priority > 100:
                bot.send_message( message.chat.id, "The priority should be between 1 - 100" )
                return 
                
        keyword_tag = message_list.index( 'keyword:' )
        reply_tag = message_list.index( 'reply:' )

        keyword_list = message_list[ keyword_tag + 1 : reply_tag ]
        reply_list = message_list[ reply_tag +1 : ]
        
        if not keyword_list or not reply_list:
            bot.send_message( message.chat.id, 'the keyword or reply should not be empty' )
            return

        save_to_config = { 'username': message.chat.username,
                           'chat_id' : message.chat.id, 
                           'keyword' : keyword_list,
                           'reply' : reply_list,
                           'priority' : priority }
                           
        logger.info( '{} add the keyword {}'.format( message.chat.username, save_to_config ) )
        value = config.get_by_path( ['autoreply'] )
        value.append( save_to_config )
        
        config.set_by_path( ['autoreply'], value )
        config.save()
        
        config.load()
        global autorepliers_list
        autorepliers_list = sorted( config.get_option( 'autoreply' ), key = lambda ls: ls['priority'], reverse=True )
        bot.send_message( message.chat.id, 'Success! Keyword list is updated.' )
        
    except Exception as e:
        bot.send_message( message.chat.id, 'Wrong format' )
        
def process_del_keyword( message ):
    try:
        index_list = re.split( ',', message.text )
        index_list = map( int, index_list )
        index_list = sorted( index_list, reverse = True )
        
        if index_list[-1] <= -1:
            bot.send_message( message.chat.id, 'Canceled.' )
            return
        
        for index in index_list:                    
            logger.info( '{} delete the keyword {}'.format( message.chat.username, autorepliers_list[ index ] ) )
            del autorepliers_list[ index ]
            
        config.set_by_path( ['autoreply'], autorepliers_list )
        config.save()
        config.load()
        bot.send_message( message.chat.id, 'Success! The keyword(s) had been deleted.' )
        
    except Exception as e:
        bot.send_message( message.chat.id, "Please send the correct index" )

def _words_in_text(word, text):
    """Return True if word is in text"""

    if word.startswith("regex:"):
        word = word[6:]
    else:
        word = re.escape(word)

    regexword = "(?<![a-zA-Z])" + word + "(?![a-zA-Z])"

    return True if re.search(regexword, text, re.IGNORECASE) else False
