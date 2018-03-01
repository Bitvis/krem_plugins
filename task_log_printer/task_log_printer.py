import os
from krempack.core import plugin

class PluginTaskLogPrinter(plugin.Plugin):
    name = "task-log-printer"

    def __init__(self):
        None

    def cli_commands(self, commands):
        commands["log"] = os.path.join(os.path.dirname(__file__), "log.cmd")
