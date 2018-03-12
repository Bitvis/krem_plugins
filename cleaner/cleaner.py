import os
from krempack.core import plugin

class PluginCleaner(plugin.Plugin):
    name = "cleaner"

    def __init__(self):
        None

    def cli_commands(self, commands):
        commands["clean"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "clean.cmd"))
