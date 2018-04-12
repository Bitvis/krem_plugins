#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil



def run(task):
    result = f.copy_setup(__file__)
    if result != rc.PASS:
        return result

    result = rc.FAIL

    os.chdir(p.TEMP_PROJECT_PATH)        
    print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

    f.shell_run("krem run -j job_foo")

    #check that 'task arguments...' is written to tasks.log
    tasks_log_path = os.path.join(p.TEMP_PROJECT_PATH, "output", "job_foo", "latest", "tasks.log")
    
    with open(tasks_log_path) as task_log_file:
        log = task_log_file.readlines()

        correct_line = "4_1  [INFO]:  task arguments: [('arg1', 'arg1_value'), ('arg2', 'arg2_value')]     [plugin:log task arguments.py]\n"

        for line in log:            
            if line == correct_line:                
                result = rc.PASS

        if result != rc.FAIL:
            print("Expected text not found in tasks.log: 4_1  [INFO]:  task arguments: [('arg1', 'arg1_value'), ('arg2', 'arg2_value')]     [plugin:log task arguments.py]")  

    return result

