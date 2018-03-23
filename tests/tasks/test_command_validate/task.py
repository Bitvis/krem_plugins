#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil
import filecmp


def validate_ok(task, path):
    result = rc.FAIL

    project_path = os.path.abspath(path)
    
    # Copy plugins to test project
    
    # get path to plugins
    plugins_path = os.path.join(project_path, "..", "..", "..")
    
    setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

    # get path to destination directory
    dest_file = os.path.join(project_path, "library", "setup.py")

    # copy setup.py file to test project
    shutil.copyfile(setup_file, dest_file)

    os.chdir(path)        
    print("Changed directory to " + str(path))


    correct_file = os.path.join(os.path.dirname(__file__), "files", "validate_ok")
    output_file = os.path.join(task.get_output_path(), "validate_ok")

    shell_return = f.shell_run_to_file("krem validate -j 0", output_file)

    if shell_return == 0:
        if filecmp.cmp(output_file, correct_file) == True:
            result = rc.PASS
        else:
            print("Files: \n{}\n{}\nare not equal".format(output_file, correct_file))
        
    return result
