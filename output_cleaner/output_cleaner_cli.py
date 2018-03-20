import os
from krempack.core import plugin

class PluginOutputCleaner(plugin.Plugin):
    name = "cleaner"

    def __init__(self):
        None

    def cli_commands(self, commands):
        commands["clean"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "clean_cmd.py"))
