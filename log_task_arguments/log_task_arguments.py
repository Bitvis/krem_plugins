#!/usr/bin/env python
## \file log_task_arguments.py
## \brief Plugin: log task arguments
'''
# Copyright (C) 2017  Bitvis AS
#
# This file is part of KREM.
#
# KREM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KREM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with KREM.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Bitvis AS 
# www.bitvis.no
# info@bitvis.no
'''

from krempack.core import plugin
import sys
import os

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger

class PluginLogTaskArguments(plugin.Plugin):
    name="log task arguments.py"

    def __init__(self):
        self.log = PluginLogger(self.name)
        


    def pre_task_function_call(self, task):

        self.log.write("task arguments: " + str(task.arguments), "info")
        



