from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''

'''Job and task plugins'''
from library.plugins.krem_plugins.print_task_results.print_task_results import PluginPrintTaskResults
from library.plugins.krem_plugins.task_tasks_log_terminal.task_tasks_log_terminal import PluginTaskTasksLogTerminal
from library.plugins.krem_plugins.time_task_function.time_task_function import PluginTimeTaskFunction
from library.plugins.krem_plugins.job_intro_text.job_intro_text import PluginJobIntroText

'''CLI plugins'''
from library.plugins.krem_plugins.task_log_printer.task_log_printer_cli import PluginTaskLogPrinter
from library.plugins.krem_plugins.help_docs.help_docs_cli import PluginHelpDocs
from library.plugins.krem_plugins.job_validator.job_validator_cli import PluginJobValidator
from library.plugins.krem_plugins.list_all.list_all_cli import PluginListAll
from library.plugins.krem_plugins.output_cleaner.output_cleaner_cli import PluginOutputCleaner
from library.plugins.krem_plugins.task_lister.task_lister_cli import PluginTaskLister


def setup_plugins(plugin_handler):
    # Register runtime plugins here
    '''
    Uncomment the following to enable some of the plugins from krem_plugins,
    or add other plugins in the same way
    '''
    #plugin_handler.register_plugin(PluginPrintTaskResults)
    #plugin_handler.register_plugin(PluginTaskTasksLogTerminal)

    #plugin_handler.register_plugin(PluginTimeTaskFunction)
    #plugin_handler.hooks["pre_task_function_call"].append_last_to_execute(PluginTimeTaskFunction)
    #plugin_handler.hooks["post_task_function_call"].append_first_to_execute(PluginTimeTaskFunction)

    #plugin_handler.register_plugin(PluginJobIntroText)
    #plugin_handler.register_plugin(PluginJobValidator)

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
    #plugin_handler.register_plugin(PluginOutputCleaner)
    #plugin_handler.register_plugin(PluginJobValidator)
    #plugin_handler.register_plugin(PluginListAll)
    pass

