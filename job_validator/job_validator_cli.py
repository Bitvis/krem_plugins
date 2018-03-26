import os
from krempack.core import plugin
from . import job_validator

class PluginJobValidator(plugin.Plugin):
    name = "validator"

    def __init__(self):
        None

    def cli_commands(self, commands):
        commands["validate"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "validate_cmd.py"))

    def cli_run_setup_arguments(self, parser):
        group = parser.add_argument_group()
        group.add_argument("--validate", action='store_true',
                           help="Validate job script before executing")

    def cli_run_execute_arguments_pre_cmd(self, args):
        if args.validate:
            validator = job_validator.Validator(args.job[0])
            if validator.run():                
                exit(1)            
