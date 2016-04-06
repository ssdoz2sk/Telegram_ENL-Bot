import asyncio, hashlib, logging, urllib, os
import urllib.parse

import urllib.request as urllib2
from http.cookiejar import CookieJar

from random import randrange, randint

import plugins

os.environ['PYTHONASYNCIODEBUG'] = '1'
logger = logging.getLogger(__name__)
bot = plugins.tracking.bot
# logger.setLevel( 'DEBUG' )
__cleverbots = dict()


""" Cleverbot API adapted from https://github.com/folz/cleverbot.py """
class Cleverbot:
    """
    Wrapper over the Cleverbot API.
    """
    HOST = "www.cleverbot.com"
    PROTOCOL = "http://"
    RESOURCE = "/webservicemin"
    API_URL = PROTOCOL + HOST + RESOURCE

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Accept-Language': 'en-us,en;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'no-cache',
        'Host': HOST,
        'Referer': PROTOCOL + HOST + '/',
        'Pragma': 'no-cache'
    }

    asked = 0
    lastanswer = ""

    def __init__(self):
        """ The data that will get passed to Cleverbot's web API """
        self.data = {
            'stimulus': '',
            'start': 'y',  # Never modified
            'sessionid': '',
            'vText8': '',
            'vText7': '',
            'vText6': '',
            'vText5': '',
            'vText4': '',
            'vText3': '',
            'vText2': '',
            'icognoid': 'wsf',  # Never modified
            'icognocheck': '',
            'fno': 0,  # Never modified
            'prevref': '',
            'emotionaloutput': '',  # Never modified
            'emotionalhistory': '',  # Never modified
            'asbotname': '',  # Never modified
            'ttsvoice': '',  # Never modified
            'typing': '',  # Never modified
            'lineref': '',
            'sub': 'Say',  # Never modified
            'islearning': 1,  # Never modified
            'cleanslate': False,  # Never modified
        }

        # the log of our conversation with Cleverbot
        self.conversation = []
        self.resp = str()
        self.asked = 0

        # install an opener with support for cookies
        cookies = CookieJar()
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
        ]
        opener = urllib2.build_opener(*handlers)
        urllib2.install_opener(opener)

        # get the main page to get a cookie (see bug  #13)
        try:
            urllib2.urlopen(Cleverbot.PROTOCOL + Cleverbot.HOST)
        except urllib2.HTTPError:
            logger.exception(e)


    def ask(self, question):
        """Asks Cleverbot a question.

        Maintains message history.

        Args:
            q (str): The question to ask
        Returns:
            Cleverbot's answer
        """
        # Set the current question
        question = question.strip()
        if not question:
            return

        if not question.endswith(("!", ",", ".", ")", "%", "*")):
            # end a sentence with a full stop
            question += "."

        self.data['stimulus'] = question
        self.asked = self.asked + 1

        # Connect to Cleverbot's API and remember the response
        try:
            self.resp = self._send()
        except urllib2.HTTPError:
            # request failed. returning empty string
            return str()

        # Add the current question to the conversation log
        self.conversation.append(question)

        parsed = self._parse()

        # Set data as appropriate
        if not self.data['sessionid']:
            self.data['sessionid'] = parsed['conversation_id']

        # Add Cleverbot's reply to the conversation log
        self.conversation.append(parsed['answer'])
        self.lastanswer = parsed['answer']

        return parsed['answer']


    def _send(self):
        """POST the user's question and all required information to the
        Cleverbot API
        Cleverbot tries to prevent unauthorized access to its API by
        obfuscating how it generates the 'icognocheck' token, so we have
        to URLencode the data twice: once to generate the token, and
        twice to add the token to the data we're sending to Cleverbot.
        """
        # Set data as appropriate
        if self.conversation:
            linecount = 1
            for line in reversed(self.conversation):
                linecount += 1
                self.data['vText' + str(linecount)] = line
                if linecount == 8:
                    break

        """XXX: unlike the original code which used an unordered dict to
        build the payload, we use an ordered string to mimic the observed
        payload during normal operation of the bot
        """
        if self.asked <= 1:
            payload = ( "stimulus={0[stimulus]}"
                        "&cb_settings_scripting=no"
                        "&islearning=1"
                        "&icognoid={0[icognoid]}" ).format(self.data)

            query_string = ""

        else:
            payload = ( "stimulus={0[stimulus]}"
                        "&vText2={0[vText2]}"
                        "&vText3={0[vText3]}"
                        "&vText4={0[vText4]}"
                        "&vText5={0[vText5]}"
                        "&vText6={0[vText6]}"
                        "&vText7={0[vText7]}"
                        "&sessionid={0[sessionid]}"
                        "&cb_settings_language=es"
                        "&cb_settings_scripting=no"
                        "&islearning={0[islearning]}"
                        "&icognoid={0[icognoid]}" ).format(self.data)

            query_string = ("out={2}"
                            "&in={0[stimulus]}"
                            "&bot=c"
                            "&cbsid={0[sessionid]}"
                            "&xai={4}"
                            "&ns={1}"
                            "&al="
                            "&dl="
                            "&flag="
                            "&user="
                            "&mode=1"
                            "&t={3}"
                            "&").format(self.data,
                                        self.asked,
                                        self.lastanswer,
                                        randint(10000, 99999),
                                        self.data["sessionid"][0:3])

        # Generate the token
        digest_txt = payload[9:35]
        token = hashlib.md5(digest_txt.encode('utf-8')).hexdigest()
        payload += "&icognocheck={}".format(token)

        # Add the token to the data
        payload = payload.encode('utf-8')
        full_url = self.API_URL + "?" + query_string
        logger.debug(payload)
        logger.debug(full_url)
        req = urllib2.Request(full_url, payload, self.headers)

        # POST the data to Cleverbot's API
        conn = urllib2.urlopen(req)
        resp = conn.read()

        # Return Cleverbot's response
        return resp

    def _parse(self):
        """Parses Cleverbot's response"""
        parsed = [
            item.split('\r') for item in self.resp.decode('utf-8').split('\r\r\r\r\r\r')[:-1]
        ]
        parsed_dict = {
            'answer': parsed[0][0],
            'conversation_id': parsed[0][1],
            'conversation_log_id': parsed[0][2],
        }
        try:
            parsed_dict['unknown'] = parsed[1][-1]
        except IndexError:
            parsed_dict['unknown'] = None

        logger.debug( "parsed_dict :{}".format( parsed_dict ) )
        return parsed_dict

@bot.message_handler( commands = ['chat'] )
def chat( message ):
    logger.warning( "TEST" )
    mes = None
    if len( message.text.split( " " ) ) == 1:
        bot.reply_to( message, "..." )
        return
    text =  cleverbot_ask( message )
    if not text:
        text = "Cleverbot is silent"
    logger.warning( text )
    bot.reply_to( message, text )

def cleverbot_ask( message, filter_ads=True):
    conv_id = str ( message.chat.id )

    if conv_id not in __cleverbots:
        __cleverbots[conv_id] = Cleverbot()
        logger.debug("added api instance for {}".format(conv_id))


    logger.warning( "__cleverbots : {} ".format( __cleverbots ) )
    message_text = " ".join( message.text.split(" ")[1:] )

    text = False
    try:
        text = __cleverbots[conv_id].ask( message_text )
        logger.debug("API returned: {}".format(text))
        if text:
            if filter_ads:
                if text.startswith("\n"):
                    # some ads appear to start with line breaks
                    text = False
                else:
                    # filter out specific ad-related keywords
                    ad_text = ["cleverscript", "cleverme", "clevertweet", "cleverenglish"]
                    for ad in ad_text:
                        if ad.lower() in text.lower():
                            logger.debug("ad-blocked")
                            text = False
                            break

    except:
        logger.exception("failed to get response")

    return text

