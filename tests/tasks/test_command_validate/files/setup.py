from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''
from library.plugins.krem_plugins.job_validator.job_validator_cli import PluginJobValidator

def setup_plugins(plugin_handler):
    plugin_handler.register_plugin(PluginJobValidator)

    pass

def setup_cli_plugins(plugin_handler):
    plugin_handler.register_plugin(PluginJobValidator)
    pass

