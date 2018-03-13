#!/usr/bin/env python
## \file time_task_function.py
## \brief Plugin: time_task_function
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
import time
import os
import datetime


pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger


class PluginTimeTaskFunction(plugin.Plugin):
    name = "time_task_function"

    def __init__(self):
        self.log = PluginLogger(self.name)

    def pre_task_function_call(self, task):
        self.log.write("started " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "info")
        data = time.clock()
        task.set_plugin_data(PluginTimeTaskFunction.name, data)


    def post_task_function_call(self, task):

        end = time.clock()

        time_taken = end - task.get_plugin_data(PluginTimeTaskFunction.name)

        str_time = "executed in {:f}s".format(time_taken)

        self.log.write(str_time, "info")
        self.log.write("stopped " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "info")





