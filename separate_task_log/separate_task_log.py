#!/usr/bin/env python
## \file separate_task_log.py
## \brief Plugin: separate task log
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
import time
import subprocess
import select

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger

class PluginSeparateTaskLog(plugin.Plugin):
    name="separate task log.py"

    def __init__(self):
        None




    def post_task_function_call(self, task):

        #this is path to file with logs from all tasks
        tasks_log_path = os.path.join(task.get_job_path(), "tasks.log")

        #this is path to log file for current task function
        task_log_path = os.path.join(task.get_job_path(), task.get_run_name(), "task.log")


        task_log_file = open(task_log_path, 'w')
        #just grab what belongs to this task
        cmd = 'cat '+tasks_log_path+' | grep ' + task.get_full_run_nr()
        subprocess.Popen(cmd, shell=True, stdout=task_log_file, stderr=task_log_file)
        



