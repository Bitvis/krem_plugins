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



class PluginTimeTaskFunction(plugin.Plugin):
    name = "time_task_function"
    start = None

    def pre_task_function_call(self, task):
        PluginTimeTaskFunction.start = time.clock()

        logger = task.get_logger()
        PluginTimeTaskFunction.run = task.get_full_run_nr()

    def post_task_function_call(self, task):
        logger = task.get_logger()

        end = time.clock()
        time_taken = end - PluginTimeTaskFunction.start

        str_time = "*** {:f}s spent by task function ({}) ***".format(time_taken, PluginTimeTaskFunction.name)

        logger.write_to_log(task.get_full_run_nr() + "  " + str_time)
