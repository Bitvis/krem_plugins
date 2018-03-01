from krempack.core import plugin

'''
    1. Change class name to a name of your choice
    2. Change plugin name
    3. Uncomment hook-functions you want to use, 
       and implement desired functionality
    4. Register the plugin in <your_krem_project>/library/setup.py>
'''

class PluginTemplate(plugin.Plugin):
    name = "plugin-name"

    def __init__(self):
        None
 
    #def job_start(self, job):

    #def pre_task_execution(self, task, job):

    #def job_progress_text(self, task, progress_text):

    #def pre_task_function_call(self, task):

    #def post_task_function_call(self, task):

    #def post_task_execution(self, task, job):

    #def job_end(self, job):

    #def cli_commands(self, commands):

    #def cli_init_setup_arguments(self, parser):

    #def cli_init_execute_arguments_pre_cmd(self, args):

    #def cli_init_execute_arguments_post_cmd(self, args):

    #def cli_run_setup_arguments(self, parser):

    #def cli_run_execute_arguments_pre_cmd(self, args):

    #def cli_run_execute_arguments_post_cmd(self, args):

    #def cli_list_setup_arguments(self, parser):

    #def cli_list_execute_arguments_pre_cmd(self, args):

    #def cli_list_execute_arguments_post_cmd(self, args):
