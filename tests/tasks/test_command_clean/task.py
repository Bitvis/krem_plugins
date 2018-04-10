#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil
import time



def clean(task):
    result = f.copy_setup(__file__)
    if result != rc.PASS:
        return result

    result = rc.FAIL

    os.chdir(p.TEMP_PROJECT_PATH)        
    print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

    f.shell_run("krem init -j job_to_clean")    
    f.shell_run("krem init -j job_not_to_clean")

    f.shell_run("krem run -j job_to_clean")
    time.sleep(1)
    f.shell_run("krem run -j job_to_clean")
    time.sleep(1)
    f.shell_run("krem run -j job_not_to_clean")

    #check that the job_to_clean_2 directory was created
    job_to_clean_path = os.path.join(p.TEMP_PROJECT_PATH, "output", "job_to_clean")
    job_not_to_clean_path = os.path.join(p.TEMP_PROJECT_PATH, "output", "job_not_to_clean")

    if os.path.isdir(job_to_clean_path) and os.path.isdir(job_not_to_clean_path):
        f.shell_run("krem clean -j job_to_clean")
        
        #now the directory should be gone
        if os.path.isdir(job_to_clean_path) or not os.path.isdir(job_not_to_clean_path):
            result = rc.FAIL
        else:
            result = rc.PASS

    return result

def clean_all(task):
    result = f.copy_setup(__file__)
    if result != rc.PASS:
        return result

    result = rc.FAIL

    os.chdir(p.TEMP_PROJECT_PATH)        
    print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

    f.shell_run("krem init -j job_to_clean_1")    
    f.shell_run("krem init -j job_to_clean_2")

    f.shell_run("krem run -j job_to_clean_1")
    time.sleep(1)
    f.shell_run("krem run -j job_to_clean_2")

    #check that the job_to_clean_x directories where created
    job_to_clean_1_path = os.path.join(p.TEMP_PROJECT_PATH, "output", "job_to_clean_1")
    job_to_clean_2_path = os.path.join(p.TEMP_PROJECT_PATH, "output", "job_to_clean_2")
    if os.path.isdir(job_to_clean_1_path) and os.path.isdir(job_to_clean_2_path):
        
        f.shell_run("krem clean --all")
        
        #now the directories should be gone
        if os.path.isdir(job_to_clean_1_path) or os.path.isdir(job_to_clean_2_path) :
            result = rc.FAIL
        else:
            result = rc.PASS

    return result