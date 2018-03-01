import os
import re

from krempack.common import kremtree
from krempack.common import constants as c

def get_task_log_path(job, nr):
    job_output_path = os.path.abspath(os.path.join(kremtree.find_common_dir(c.PROJECT_OUTPUT_DIR), job))
    job_instances = []
    target_path = None
    target_job_instance = None

    if not os.path.isdir(job_output_path):
        print("[ERROR]: No output directory found for provided job")
        exit(1)

    for entry in os.listdir(job_output_path):
        if os.path.isdir(os.path.join(job_output_path, entry)) and re.match("\d+_\d+", entry):
            job_instances.append(entry.strip())

    if len(job_instances) > nr:
        job_instances.sort(reverse=True)
        target_job_instance = job_instances[nr]
        
        target_path = os.path.join(job_output_path, target_job_instance, "tasks.log")
        if not os.path.isfile(target_path):
            target_path = None


    return (target_job_instance, target_path)

def id_job(target):
    jobs_path = kremtree.find_common_dir(c.PROJECT_JOBS_DIR)
    num = -1
    if isinstance(target, int):
        num = target
    elif isinstance(target, str) and target.isdigit():
        num = int(target)

    if not num < 0:
        jobs = kremtree.list_dir(jobs_path)
        if not num + 1 > len(jobs):
            idx = 0
            for job in jobs:
                if idx == num:
                    print("Job[" + str(num) + "]: " + str(job))
                    target = job
                    break
                idx = idx + 1
        else:
            print("Invalid job number: " + str(num))

    return target

def display_task_log(job, run_nr, last):

    job = id_job(job)

    if not last:
        last = 0

    job_instance, task_log_path = get_task_log_path(job, int(last))
    
    if job_instance is None:
        print("[ERROR]: Job instance output directory not found.")
        exit(1)
    elif task_log_path is None:
        print("[ERROR]: Job instance output directory found, but it does not contain a 'tasks.log' file ")
        exit(1)
    else:
        cmd = "cat " + task_log_path
        if run_nr is not None:
            cmd = cmd + " | grep -G ^" + run_nr

        print("Task log from job instance '" + os.path.join(job,job_instance) + "'")
        if run_nr is not None:
            print("Run number: " + run_nr)

        print("")
        print("------------------------------------------------------")
        os.system(cmd)
        print("------------------------------------------------------")
        
