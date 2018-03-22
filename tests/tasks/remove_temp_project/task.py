#!/bin/env python

import os
import shutil

from library.returncodes import *

def run(task, path):
    path = os.path.abspath(path)
    result = rc.FAIL
    # Init test project    
    
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)
            print("Removed directory: " + str(path))
            result = rc.PASS
        except Exception:
            print("ERROR: Failed to remove " + str(path))
            result = rc.FAIL
    else:
        print("WARNING: " + path + " does not exist.")
        result = rc.SKIPPED
        
    return result

