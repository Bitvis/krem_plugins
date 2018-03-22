#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil


def run(task, path):
    project_path = os.path.abspath(path)
    
    # Copy plugins to test project
    
    # get path to plugins
    plugins_path = os.path.join(project_path, "..", "..", "..")
    

    setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

    # get path to destination directory
    dest_file = os.path.join(project_path, "library", "setup.py")

    try:
        shutil.copyfile(setup_file, dest_file)        
    except Exception:
        return rc.FAIL

    return rc.PASS

