from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''
from library.plugins.krem_plugins.print_task_results.print_task_results import PluginPrintTaskResults
from library.plugins.krem_plugins.debug_terminal.debug_terminal import PluginDebugTerminal
from library.plugins.krem_plugins.help_docs.help_docs import PluginHelpDocs
from library.plugins.krem_plugins.task_lister.task_lister import PluginTaskLister
from library.plugins.krem_plugins.task_log_printer.task_log_printer import PluginTaskLogPrinter
from library.plugins.krem_plugins.time_task_function.time_task_function import PluginTimeTaskFunction
from library.plugins.krem_plugins.cleaner.cleaner import PluginCleaner
from library.plugins.krem_plugins.job_intro_text.job_intro_text import PluginJobIntroText
from library.plugins.krem_plugins.validator.validator import PluginValidator

def setup_plugins(plugin_handler):
    # Register runtime plugins here
    '''
    Uncomment the following to enable some of the plugins from krem_plugins,
    or add other plugins in the same way
    '''
    #plugin_handler.register_plugin(PluginPrintTaskResults)
    #plugin_handler.register_plugin(PluginDebugTerminal)
    #plugin_handler.register_plugin(PluginTimeTaskFunction)
    #plugin_handler.register_plugin(PluginJobIntroText)
    #plugin_handler.register_plugin(PluginValidator)

    pass

def setup_cli_plugins(plugin_handler):
    # Register CLI plugins here
    '''
    Uncomment the following to enable some of the plugins from krem_plugins,
    or add other plugins in the same way
    '''
    #plugin_handler.register_plugin(PluginHelpDocs)
    #plugin_handler.register_plugin(PluginTaskLister)
    #plugin_handler.register_plugin(PluginTaskLogPrinter)
    #plugin_handler.register_plugin(PluginCleaner)
    #plugin_handler.register_plugin(PluginValidator)
    pass
