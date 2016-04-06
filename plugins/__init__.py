import asyncio, importlib, os, sys, logging
import inspect
logger = logging.getLogger( __name__ )

class tracker( object ):
    def __init__( self ):
        self.bot = None
        self.config = None
        self.list = {}
        
    def setting( self, bot, config ):
        self.bot = bot
        self.config = config
        
tracking = tracker()

def load( bot, module_path, module_name = None ):
    if module_name is None:
        module_name = module_path.split(".")[-1]

    if module_path in tracking.list:
        raise RuntimeError("{} already loaded".format(module_path))

    try:
        if module_path in sys.modules:
            plugin = importlib.reload( sys.modules[ module_path ])
            logger.debug( "reloading {}".format( module_path ) )
        else:
            plugin = importlib.import_module(module_path)
            logger.debug( "importing {}".format( module_path ) )

    except Exception as e:
        logger.exception("EXCEPTION during plugin import: {}".format(module_path))
        return

    public_function = [ o for o in inspect.getmembers( sys.modules[ module_path ], inspect.isfunction ) ]
    logger.debug( " ".join( [ o[0] for o in public_function ] ) )
    tracking.list[ module_path ] = public_function
    
def retrieve_all_plugins( plugin_path = None, must_start_with = None ):
    if not plugin_path:
        plugin_path = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep + "plugins"
    plugin_list =[]
    nodes = os.listdir( plugin_path )

    for node_name in nodes:
        full_path = os.path.join(plugin_path, node_name)
        module_names = [ os.path.splitext(node_name)[0] ] # node_name without .py extension

        if node_name.startswith(("_", ".")):
            continue

        if must_start_with and not node_name.startswith(must_start_with):
            continue

        if os.path.isfile(full_path):
            if not node_name.endswith(".py"):
                continue
        else:
            if not os.path.isfile(os.path.join(full_path, "__init__.py")):
                continue

            for sm in retrieve_all_plugins(full_path, must_start_with=node_name):
                module_names.append(module_names[0] + "." + sm)

        plugin_list.extend(module_names)

    logger.debug("retrieved {}: {}.{}".format(len(plugin_list), must_start_with or "plugins", plugin_list))
    return plugin_list

def get_configured_plugins( bot ):
    all_plugins = retrieve_all_plugins()
    plugin_list = all_plugins

    logger.info("included {}: {}".format(len(plugin_list), plugin_list))

    return plugin_list

def load_user_plugins( bot ):
    plugin_list = get_configured_plugins( bot )
    for module in plugin_list:
        module_path = "plugins.{}".format( module )
        load( bot, module_path )
