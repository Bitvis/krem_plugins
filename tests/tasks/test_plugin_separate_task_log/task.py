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

    #check that the task.log file was created
    task_log_path = os.path.join(p.TEMP_PROJECT_PATH, "output", "job_foo", "latest", "1_1_task_foo_run_without_arguments", "task.log")
    if os.path.isfile(task_log_path):
        if os.stat(task_log_path).st_size == 0:
            print("task log file (" + task_log_path + ") is empty!!!")
            result = rc.FAIL
        else:
            with open(task_log_path) as task_log_file:
                log = task_log_file.readlines()

            result = rc.PASS          

            print("task log (all lines must start with '1_1' to pass):")  
            for line in log:            
                print(line)
                if line[0:3] != "1_1":                
                    result = rc.FAIL
    else:
        result = rc.FAIL

    return result

