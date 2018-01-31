#!/usr/bin/env python
## \file print_task_variables.py
## \brief Plugin: print task variables
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
class PluginPrintTaskVariables(plugin.Plugin):
    name="print_task_results"

    def pre_task_execution(self, task, job):
        logger = job.config.get_job_logger()
        logger. write("variables: " + task.get_task_name() + ": " + str(task.get_variables()), "info")

            