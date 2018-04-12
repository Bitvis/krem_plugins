from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''

'''Job and task plugins'''
from library.plugins.krem_plugins.log_task_arguments.log_task_arguments import PluginLogTaskArguments


def setup_plugins(plugin_handler):
    # Register runtime plugins here
    
    plugin_handler.register_plugin(PluginLogTaskArguments) 


def setup_cli_plugins(plugin_handler):
    pass

