#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil
import filecmp


def copy_setup():
    result = rc.FAIL

    try:
        setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

        # get path to destination directory
        dest_file = os.path.join(p.TEMP_PROJECT_PATH, "library", "setup.py")

        # copy setup.py file to test project
        shutil.copyfile(setup_file, dest_file)
        #remove *.pyc file so it gets updated after copying the setup.py file
        os.remove(dest_file + 'c')
        result = rc.PASS
    except:
        result = rc.FAIL

    return result


def clean_job(task):
    result = copy_setup()
    if result != rc.PASS:
        return result

    os.chdir(p.TEMP_PROJECT_PATH)        
    print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

    shell_return = f.shell_run("krem clean -j 0")

    if(shell_return == 0):
        result = rc.PASS
    else:
        result = rc.FAIL
        
    return result
