#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
from shutil import copyfile


def run(task):
    result = rc.FAIL

    start_directory = os.getcwd()

    # Navigate to temp project dir and run
    os.chdir(p.TEMP_PROJECT_PATH)
    print("Changed directory to " + str(p.TEMP_PROJECT_PATH))
    shell_return = f.shell_run("krem run -j 0")

    if shell_return[0] == 0:
        result = rc.PASS        
    

    return result

