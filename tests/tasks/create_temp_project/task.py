import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
from shutil import copyfile


def run(task):
    
    result = rc.FAIL
    # Init test project    
    shell_return = f.shell_run("krem init -p " + p.TEMP_PROJECT_PATH)
    
    if shell_return[0] == 0:
        # Navigate to temp project dir and run
        os.chdir(p.TEMP_PROJECT_PATH)

        result = rc.PASS
        print("Changed directory to " + str(p.TEMP_PROJECT_PATH))
        shell_return = f.shell_run("krem init -j job_foo")
        if shell_return[0] != 0:
            result = rc.FAIL   
        
        shell_return = f.shell_run("krem init -t task_foo")
        if shell_return[0] != 0:
            result = rc.FAIL               

                

    return result

