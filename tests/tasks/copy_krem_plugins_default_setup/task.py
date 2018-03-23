#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil


def run(task):
    # Copy plugins to test project
    
    setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

    # get path to destination directory
    dest_file = os.path.join(p.TEMP_PROJECT_PATH, "library", "setup.py")

    try:
        shutil.copyfile(setup_file, dest_file)        
    except Exception:
        return rc.FAIL

    return rc.PASS

