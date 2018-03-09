
from krempack.core import plugin

from . import listlib
class PluginTaskLister(plugin.Plugin):
    name = "task-lister"

    def __init__(self):
        None

    def cli_list_setup_arguments(self, parser):
        group = parser.add_argument_group()

        group.add_argument("--job-tasks", nargs=1,
                           help="Lists tasks used in target job")

    def cli_list_execute_arguments_pre_cmd(self, args):
        if args.job_tasks is not None:
            listlib.run(args.job_tasks[0])
