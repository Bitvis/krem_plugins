#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil


def run(task, path):
    result = rc.PASS

    project_path = os.path.abspath(path)
    
    # Copy plugins to test project
    
    # get path to plugins
    plugins_path = os.path.join(project_path, "..", "..", "..")
    
    setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

    # get path to destination directory
    dest_file = os.path.join(project_path, "library", "setup.py")

    try:
        # copy setup.py file to test project
        shutil.copyfile(setup_file, dest_file)

        os.chdir(path)        
        print("Changed directory to " + str(path))
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + path + "'")

    if result == rc.PASS:
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
