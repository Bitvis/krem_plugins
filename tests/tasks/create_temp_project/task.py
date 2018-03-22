import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
from shutil import copyfile


def run(task, path):
    project_path = os.path.abspath(path)
    result = rc.FAIL
    # Init test project    
    shell_return = f.shell_run("krem init -p " + project_path)
    
    if shell_return[0] == 0:
        path = os.path.abspath(path)    

        # Navigate to temp project dir and run
        os.chdir(path)

        result = rc.PASS
        print("Changed directory to " + str(path))
        shell_return = f.shell_run("krem init -j job_foo")
        if shell_return[0] != 0:
            result = rc.FAIL   
        
        shell_return = f.shell_run("krem init -t task_foo")
        if shell_return[0] != 0:
            result = rc.FAIL               

                

    return result

