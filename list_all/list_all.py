from krempack.core import plugin
from . import lalib

class PluginListAll(plugin.Plugin):

    name = "list-all"

    def __init__(self):
        None

    def cli_list_setup_arguments(self, parser):
        group = parser.add_argument_group()
        group.add_argument("-a", "--all", action='store_true', help="List all jobs and tasks")

    def cli_list_execute_arguments_pre_cmd(self,args):

        if args.all is True:
            lalib.list_all()