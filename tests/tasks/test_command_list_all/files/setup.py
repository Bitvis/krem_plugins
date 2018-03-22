from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''
'''CLI plugins'''
from library.plugins.krem_plugins.list_all.list_all_cli import PluginListAll


def setup_plugins(plugin_handler):
    pass

def setup_cli_plugins(plugin_handler):
    plugin_handler.register_plugin(PluginListAll)
    pass

