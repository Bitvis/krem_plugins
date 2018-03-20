import os
from krempack.core import plugin
from krempack.common import kremtree

class PluginHelpDocs(plugin.Plugin):
    name = "help-docs"

    def __init__(self):
        None

    def cli_commands(self, commands):
        commands["help"] = os.path.join(os.path.dirname(__file__), "help_cmd.py")
