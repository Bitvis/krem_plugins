#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil
import filecmp


def copy_setup(task):
    result = rc.FAIL

    try:
        setup_file = os.path.join(os.path.dirname(__file__), "files", "setup.py")

        # get path to destination directory
        dest_file = os.path.join(p.TEMP_PROJECT_PATH, "library", "setup.py")

        # copy setup.py file to test project
        shutil.copyfile(setup_file, dest_file)
        #remove *.pyc file so it gets updated after copying the setup.py file
        if os.path.exists(dest_file + 'c'):
            os.remove(dest_file + 'c')
        result = rc.PASS
    except:
        result = rc.FAIL

    return result

def copy_job(job):
    result = rc.FAIL

    try:
        job_dir = os.path.join(os.path.dirname(__file__), "files", job)

        # get path to destination directory
        jobs_dir = os.path.join(p.TEMP_PROJECT_PATH, "jobs", job)

        # copy job file to test project
        shutil.copytree(job_dir, jobs_dir)
        
        result = rc.PASS
    except:
        print("Could not copy job: " + job_dir + "\nto: " + jobs_dir)
        result = rc.FAIL

    return result


def validate_ok(task):
    
    os.chdir(p.TEMP_PROJECT_PATH)        

    correct_file = os.path.join(os.path.dirname(__file__), "files", "validate_ok_output")
    output_file = os.path.join(task.get_output_path(), "validate_output")
    
    shell_return = f.shell_run_to_file("krem validate -j 0", output_file)
    
    if shell_return == 0:
        if filecmp.cmp(output_file, correct_file) == True:
            result = rc.PASS
        else:
            print("Files: \n{}\n{}\nare not equal".format(output_file, correct_file))
            result = rc.FAIL
        
    return result

def job_missing_start(task):
    result = rc.FAIL

    if copy_job("job_missing_start") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_start")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_missing_end(task):
    result = rc.FAIL

    if copy_job("job_missing_end") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_end")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_missing_parallel_task(task):
    result = rc.FAIL

    if copy_job("job_missing_parallel_task") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_parallel_task")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_missing_wait_for_complete(task):
    result = rc.FAIL

    if copy_job("job_missing_wait_for_complete") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_wait_for_complete")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_missing_task(task):
    result = rc.FAIL

    if copy_job("job_missing_task") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_task")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_missing_task_function(task):
    result = rc.FAIL

    if copy_job("job_missing_task_function") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_task_function")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_missing_task_arguments(task):
    result = rc.FAIL

    if copy_job("job_missing_task_arguments") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_missing_task_arguments")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_add_task_after_end(task):
    result = rc.FAIL

    if copy_job("job_add_task_after_end") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_add_task_after_end")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_add_task_before_start(task):
    result = rc.FAIL

    if copy_job("job_add_task_before_start") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_add_task_before_start")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result


def job_multiple_start(task):
    result = rc.FAIL

    if copy_job("job_multiple_start") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_multiple_start")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result   
    

def job_multiple_end(task):
    result = rc.FAIL

    if copy_job("job_multiple_end") == rc.PASS:

        os.chdir(p.TEMP_PROJECT_PATH)        

        shell_return, output = f.shell_run("krem validate -j job_multiple_end")

        if shell_return != 0:
            # krem validate should fail in this test
            result = rc.PASS
        
    return result      