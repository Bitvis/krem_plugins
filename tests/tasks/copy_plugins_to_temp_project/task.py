#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil


def run(task):
    # Copy plugins to test project
    
    # get path to plugins
    plugins_path = os.path.join(p.TEMP_PROJECT_PATH, "..", "..", "..")
    
    # get path to destination directory
    krem_plugins_dir = os.path.join(p.TEMP_PROJECT_PATH, "library", "plugins", "krem_plugins")

    try:
        IGNORE_PATTERNS = ('tests','__pycache__','.gitignore','.git','.pyc','.vscode') 
        shutil.copytree(plugins_path, krem_plugins_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))
    except:
        return rc.FAIL

    return rc.PASS
