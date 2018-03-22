

import sys
import os
import time
from krempack.core import kjob
from library.returncodes import *
import time

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
from library.testlib import parameters as p

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)

    # Initialize job
    job.start()

    temp_project_path = ("path", p.TEMP_PROJECT_PATH)

    job.run_task_serial('remove_temp_project', 'run', arguments=[temp_project_path])

    if rc.PASS == job.run_task_serial('create_temp_project', 'run', arguments=[temp_project_path]):
        job.run_task_serial('copy_plugins_to_temp_project', 'run', arguments=[temp_project_path])        
        
        # run job in temp project with default setup.py, just to check it everything is ok before we modify setup.py
        job.run_task_serial('run_job', 'run', arguments=[temp_project_path])        
        job.run_task_serial('copy_krem_plugins_default_setup', 'run', arguments=[temp_project_path])
        
        # sometimes running run_job close after each other may result in the same output timestamp
        # waiting 1 sec will prevent that
        time.sleep(1)
        if rc.PASS == job.run_task_serial('run_job', 'run', arguments=[temp_project_path]):
            job.run_task_serial('test_command_list_all', 'run', arguments=[temp_project_path])

            job.run_task_serial('test_command_validate', 'validate_ok', arguments=[temp_project_path])

    # Finalize job
    job.end()

    task_results = job.get_task_results()
    #we expect each result to be '0' so if the sum of all results is more than 0 then at least one of the tasks failed
    if sum(task_results) > 0:
        err = rc.FAIL
    else:
        err = rc.PASS
    
    exit(err)
    
