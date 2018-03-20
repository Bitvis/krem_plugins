#!/usr/bin/env python
## \file print_task_results.py
## \brief Plugin: print task results
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

class PluginPrintTaskResults(plugin.Plugin):
    name="print_task_results"

    def __init__(self):
        None

    def post_task_execution(self, task, job):
        log = PluginLogger(self.name, job_log=job.log)
        task_result = job.config.get_return_code_parser().parse(task.get_task_result())

        text = '{0:8}{1}'.format(task.get_full_run_nr(), task_result)

        # overwriting default logger format as defined in krem_plugins_config.py
        plugin_logger_ec_format = [ {"property" : "log_entry",   "format": "{}".format("{input}"), "enabled": True},
                                    {"property" : "", "format": "", "enabled": False},]

        log.write(text, "info", logger_format=plugin_logger_ec_format)


