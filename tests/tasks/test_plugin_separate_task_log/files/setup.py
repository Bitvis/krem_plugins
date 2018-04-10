from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''

from library.plugins.krem_plugins.separate_task_log.separate_task_log import PluginSeparateTaskLog

def setup_plugins(plugin_handler):
    plugin_handler.register_plugin(PluginSeparateTaskLog)
    plugin_handler.hooks["post_task_function_call"].append_last_to_execute(PluginSeparateTaskLog)

def setup_cli_plugins(plugin_handler):
    pass

