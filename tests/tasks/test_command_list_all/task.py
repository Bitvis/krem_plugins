#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil


def copy_setup():
    result = rc.PASS

    setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

    # get path to destination directory
    dest_file = os.path.join(p.TEMP_PROJECT_PATH, "library", "setup.py")

    try:
        # copy setup.py file to test project
        shutil.copyfile(setup_file, dest_file)
        #remove *.pyc file so it gets updated after copying the setup.py file
        os.remove(dest_file + 'c')
        result = rc.PASS
    except:
        result = rc.FAIL

    return result


def run(task):
    result = copy_setup()
    if result != rc.PASS:
        print("nok")
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
