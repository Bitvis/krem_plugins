from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''
from library.plugins.krem_plugins.output_cleaner.output_cleaner_cli import PluginOutputCleaner


def setup_plugins(plugin_handler):
    pass

def setup_cli_plugins(plugin_handler):
    plugin_handler.register_plugin(PluginOutputCleaner)
    pass

