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

    shell_return, output = f.shell_run("krem list -a")
    
    if shell_return == 0:
        correct_output = []
        correct_output.append("Available jobs: \n")
        correct_output.append("[nr]\tname\n")
        correct_output.append("[0]\tjob_foo\n")
        correct_output.append("Available tasks:\n")
        correct_output.append("[nr]\tname\n")
        correct_output.append("[0]\ttask_foo\n")
        
        correct_line_count = 0
        for line in output:
            if line in correct_output:
                correct_line_count += 1             

        if correct_line_count == 6:
            result = rc.PASS
    
            
    return result
