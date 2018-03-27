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
jobs_dir = kremtree.find_common_dir(c.PROJECT_JOBS_DIR)

def id_job(target):    
    num = -1
    if isinstance(target, int):
        num = target
    elif isinstance(target, str) and target.isdigit():
        num = int(target)

    if not num < 0:
        jobs = kremtree.list_dir(jobs_dir)
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
            target = None

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
        log.write("Removed: " + target, "info")
        success = True
    except Exception as e:
        log.write("Failed to remove '{}'. Exception raised: {}".format(target, str(e)), "error")
        success = False

    return success

def remove_targets(targets):
    # MICHAL: ma ha success?
    success = True
    for target in targets:
        success = remove_target(target) and success

def unexpected_in_job_dir(dir):
    unexpected_targets = []    

    for entry in os.listdir(dir):            
        path = os.path.join(dir, entry)            
        if os.path.isfile(path) or (not re.match("\d+_\d+", entry) and not "latest" in entry):
            unexpected_targets.append(os.path.join(dir, entry))                                
                    
    return unexpected_targets

def unexpected_in_output_dir(dir):
    unexpected_targets = []

    for entry in os.listdir(dir):
        path = os.path.join(dir, entry)
        if os.path.isfile(path) and entry != "info":
            unexpected_targets.append(entry)                
        else:
            #check if there is a job with the same name as the directory
            if entry not in os.listdir(jobs_dir):
                unexpected_targets.append(entry)                

    return unexpected_targets

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
    job_dir = job    

    if not os.path.isdir(job_dir):
        log.write("Nothing to remove", "info")
        success = True
    else:    
        if keep:
            for entry in os.listdir(job_dir):
                if os.path.basename(entry) != "latest":
                    rm_targets.append(entry)

            keep_job_instances(rm_targets, keep)

            for index in range(len(rm_targets)):
                rm_targets[index] = os.path.join(job_dir, rm_targets[index])

            success = True
        else:  
            unexpected_targets = unexpected_in_job_dir(job_dir)
            if len(unexpected_targets) == 0 or force:
                rm_targets.append(job_dir)
                success = True
            else:
                for entry in unexpected_targets:
                    log.write("Unexpected entry: {}.".format(os.path.join(output_dir, entry)), "error")
                success = False  
        
        remove_targets(rm_targets)

    return success

def clean(jobs, force, keep):
    success = True

    for job in jobs:
        job = id_job(job)
        if job is not None:
            job = os.path.join(output_dir, job)        
            success = clean_target_job(job, force, keep) and success        
        else:
            success = False
    return success


def clean_all(force, keep): 
    success = True   
    rm_targets = []
    unexpected_targets = []
    
    if not force:
        # find all unexpected entries in output
        unexpected_targets = unexpected_in_output_dir(output_dir)
    
    # find all expected entries
    for entry in os.listdir(output_dir):
        if entry not in unexpected_targets:            
            rm_targets.append(os.path.join(output_dir, entry))

    # remove all expected entries
    for rm_target in rm_targets:        
        if os.path.isdir(rm_target): 
            clean_target_job(rm_target, force, keep)
        else:
            remove_target(rm_target)

    if not force:
        if len(unexpected_targets) > 0:
            for entry in unexpected_targets:
                log.write("Unexpected entry: {}.".format(os.path.join(output_dir, entry)), "error")
            
            log.write("Add argument '-f' to force remove all", "info")
            success = False               

    return success
    


    

    
