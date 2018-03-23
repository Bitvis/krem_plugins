#!/bin/env python

import os
import shutil

from library.returncodes import *
from library.testlib import parameters as p

def run(task):
    
    result = rc.FAIL
    # Init test project    
    
    if os.path.isdir(p.TEMP_PROJECT_PATH):
        try:
            shutil.rmtree(p.TEMP_PROJECT_PATH)
            print("Removed directory: " + str(p.TEMP_PROJECT_PATH))
            result = rc.PASS
        except Exception:
            print("ERROR: Failed to remove " + str(p.TEMP_PROJECT_PATH))
            result = rc.FAIL
    else:
        print("WARNING: " + p.TEMP_PROJECT_PATH + " does not exist.")
        result = rc.SKIPPED
        
    return result

