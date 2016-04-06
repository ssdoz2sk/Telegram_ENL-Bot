import argparse, json, logging, logging.config, os

import telebot
import config
import version
import plugins


API_TOKEN = 'TOKEN'
logger = logging.getLogger()

def run_bot( config_path ):
    conf = config.Config( config_path )
    bot = telebot.TeleBot( API_TOKEN )
    plugins.tracking.setting( bot, conf )
    plugins.load_user_plugins( bot )

    bot.polling( none_stop = True )
    conf.flush()
    
def configure_logging( args ):
    log_level = 'DEBUG' if args.debug else 'INFO'

    default_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(levelname)s %(name)s: %(message)s',
                'datefmt': '%H:%M:%S'
            },
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'level': log_level, # 'INFO',
                'formatter': 'console'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': args.log,
                'level': log_level,
                'formatter': 'default',
            }
        },
        'loggers': {
            # root logger
            '': {
                'handlers': ['file', 'console'],
                'level': log_level
            },
            'requests': { 'level': 'WARNING'},
            'urllib3': { 'level' : 'WARNING' },
            'plugins': { 'level' : 'DEBUG'}
        }
    }

    logging_config = default_config

    bootcfg = config.Config( args.config )
    if bootcfg.exists( [ "logging.system" ] ):
        logging_config = bootcfg[ "logging.system" ]

    logging.config.dictConfig( logging_config )

    logger = logging.getLogger()
    if args.debug:
        logger.setLevel( logging.DEBUG )
    logger.warning( "log_level is {}".format( log_level ))

def main():

    default_log_path = os.path.join( os.path.dirname( __file__ ), 'TelegramBot.log')
    default_config_path = os.path.join( os.path.dirname( __file__ ), 'config.json')

    parser = argparse.ArgumentParser( prog = 'TelegramBot', formatter_class = argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument( '-d', '--debug', action='store_true',           help=( 'log detailed debugging messages' ) )
    parser.add_argument( '--log',         default=default_log_path,      help=( 'log file path' ) )
    parser.add_argument( '--config',      default=default_config_path,   help=( 'config storage path' ) )
    parser.add_argument( '--version',     action='version', version='%(prog)s {}'.format( version.__version__), help=( 'show program\'s version number and exit' ) )
    args = parser.parse_args()

    configure_logging( args )
    run_bot( args.config )
    
if __name__ == '__main__':
    main()
