import os
import re
import sys
import shutil
from krempack.common import kremtree
from krempack.common import constants as c

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger

log = PluginLogger("cleaner")
output_dir = kremtree.find_common_dir(c.PROJECT_OUTPUT_DIR)

def id_job(target):
    jobs_path = kremtree.find_common_dir(c.PROJECT_JOBS_DIR)
    num = -1
    if isinstance(target, int):
        num = target
    elif isinstance(target, str) and target.isdigit():
        num = int(target)

    if not num < 0:
        jobs = kremtree.list_dir(jobs_path)
        jobs.sort()
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

def remove_target(target):
    success = False
    try:
        if os.path.isfile(target):
            os.remove(target)
        elif os.path.islink(target):
            os.unlink(target)
        else:
            shutil.rmtree(target)
        success = True
        log.write("Removed: " + target, "info")
    except Exception as e:
        log.write("Failed to remove '{}'. Exception raised: {}".format(target, str(e)), "error")

    return success

def remove_targets(targets):
    success = True
    for target in targets:
        success = remove_target(target) and success

def unexpected_in_job_dir(dir, force):
    found = False

    if not force:
        for entry in os.listdir(dir):
            path = os.path.join(dir, entry)
            if os.path.isfile(path) or (not re.match("\d+_\d+", entry) and not "latest" in entry):
                log.write("Unexpected entry: {}. Add argument '-f' to force remove".format(os.path.join(dir, entry)), "error")
                found = True
                
    return found

def unexpected_in_output_dir(dir, force):
    found = False

    if not force:
        for entry in os.listdir(dir):
            path = os.path.join(dir, entry)
            if os.path.isfile(path) and ".gitignore" not in entry and "info" not in entry:
                log.write("Unexpected entry: {}. Add argument '-f' to force remove".format(os.path.join(dir, entry)), "error")
                found = True
                
    return found

def keep_job_instances(target_list, keep):
    if keep:
        keep = int(keep[0])
        output_instances = []

        for entry in target_list:
            if re.match("\d+_\d+", entry):
                output_instances.append(entry)

        output_instances.sort()

        if keep >= len(output_instances):
            to_keep = output_instances
        else:
            to_keep = output_instances[-keep:]

        for instance in to_keep:
            target_list.remove(instance)

        

def clean_target_job(job, force=False, keep=None):
    success = False
    rm_targets = []
    job_dir = os.path.join(output_dir, job)

    if keep:
        for entry in os.listdir(job_dir):
            rm_targets.append(entry)

        keep_job_instances(rm_targets, keep)

        for index in range(len(rm_targets)):
            rm_targets[index] = os.path.join(job_dir, rm_targets[index])

    else:
        if not unexpected_in_job_dir(job_dir, force):
            rm_targets.append(job_dir)

    remove_targets(rm_targets)

    return success

def clean(jobs, force, keep):
    err = False

    if not jobs:
        log.write("No target jobs to clean.", "error")
        err = True
    else:
        for job in jobs:
            job = id_job(job)
            err = not clean_target_job(job, force, keep) and not err

    exit(err)

def clean_all(force, keep):
    success = False
    rm_targets = []
    
    if not unexpected_in_output_dir(output_dir, force):
        for entry in os.listdir(output_dir):
            if not ".gitignore" in entry:
                rm_targets.append(entry)

    for rm_target in rm_targets:
        if "info" in rm_target and os.path.isfile(os.path.join(output_dir, rm_target)):
            if not keep:
                remove_target(os.path.join(output_dir, rm_target))
        elif os.path.isfile(os.path.join(output_dir, rm_target)):
            remove_target(os.path.join(output_dir, rm_target))
        else:
            clean_target_job(rm_target, force, keep)

    

    
