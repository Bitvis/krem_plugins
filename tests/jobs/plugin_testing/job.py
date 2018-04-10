

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

    job.run_task_serial('remove_temp_project', 'run')

    if rc.PASS == job.run_task_serial('create_temp_project', 'run'):
        job.run_task_serial('copy_plugins_to_temp_project', 'run')        
        
        # run job in temp project with default setup.py, just to check it everything is ok before we modify setup.py
        job.run_task_serial('run_job', 'run')        
        job.run_task_serial('copy_krem_plugins_default_setup', 'run')
        
        # sometimes running run_job close after each other may result in the same output timestamp
        # waiting 1 sec will prevent that
        time.sleep(1)
        if rc.PASS == job.run_task_serial('run_job', 'run'):
            job.run_task_serial('test_command_clean', 'clean')
            job.run_task_serial('test_command_clean', 'clean_all')

            job.run_task_serial('test_command_list_all', 'run')
            
            job.run_task_serial('test_command_validate', 'copy_setup')
            job.run_task_serial('test_command_validate', 'validate_ok')
            job.run_task_serial('test_command_validate', 'job_missing_start')
            job.run_task_serial('test_command_validate', 'job_missing_end')
            job.run_task_serial('test_command_validate', 'job_missing_parallel_task')
            job.run_task_serial('test_command_validate', 'job_missing_wait_for_complete')
            job.run_task_serial('test_command_validate', 'job_missing_task')
            job.run_task_serial('test_command_validate', 'job_missing_task_function')
            job.run_task_serial('test_command_validate', 'job_missing_task_arguments')
            job.run_task_serial('test_command_validate', 'job_add_task_after_end')
            job.run_task_serial('test_command_validate', 'job_add_task_before_start')
            job.run_task_serial('test_command_validate', 'job_multiple_start')
            job.run_task_serial('test_command_validate', 'job_multiple_end')

            job.run_task_serial('test_plugin_separate_task_log', 'run')

            

    # Finalize job
    job.end()

    task_results = job.get_task_results()
    #we expect each result to be '0' so if the sum of all results is more than 0 then at least one of the tasks failed
    if sum(task_results) > 0:
        err = rc.FAIL
    else:
        err = rc.PASS
    
    exit(err)
    
