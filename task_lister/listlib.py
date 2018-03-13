import os
import re
import sys
from krempack.common import kremtree
from krempack.common import constants as c

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger

log = PluginLogger("task_lister")

def analyse_file(path):
    file = open(path, 'r')
    tasklist = []

    run_task_calls = []
    comment_lines_detect = False
    for line in file.readlines():
        line = line.strip()

        if not comment_lines_detect and "'''" in line:
            comment_lines_detect = True
        elif comment_lines_detect and "'''" in line:
            comment_lines_detect = False

        if not comment_lines_detect:
            match = re.match("#", line)
            if not match and "run_task" in line:
                match = re.search(r"\((.*),(.*)(,|\))", line, re.M|re.I)
                if match:
                    param_list = match.group().strip("(").strip(")").split(",")
                    call_params = [param_list[0].strip(), param_list[1].strip()]
                    run_task_calls.append(call_params)
                else:
                    log.write("Incorrect call to run_task in given job. Function call: " + str(line), 'error')


    for call in run_task_calls:
        task_exists = False
        for task in tasklist:
            if call[0] == task["taskname"] and call[1] == task["function"]:
                task_exists = True

        if not task_exists:
            tasklist.append({"taskname": call[0], "function": call[1]})

    return tasklist

def print_task_list(tasklist):
    longest_task_name = 0
    for task in tasklist:
        if len(task["taskname"]) > longest_task_name:
            longest_task_name = len(task["taskname"])

    log.write("")
    print_string = "{:>2}{:>4}{:>" + str((longest_task_name + 4)) + "}{:>" + str((longest_task_name + 6)) + "}"
    log.write(print_string.format("", "Task", "", "Function"))
    log.write("")

    for task in tasklist:
        variable_task_name = ""
        variable_function_name = ""
        name = task["taskname"]
        function = task["function"]

        if name[:1] != "'" and name[:1] != '"':
            variable_task_name = "*"
        else:
            name = name.strip("'").strip('"')
        if function[:1] != "'" and function[:1] != '"':
            variable_function_name = "*"
        else:
            function = function.strip("'").strip('"')

        log.write(print_string.format(variable_task_name, name, variable_function_name, function))

    log.write("")

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
                    log.write("Job[" + str(num) + "]: " + str(job), 'info')
                    target = job
                    break
                idx = idx + 1
        else:
            log.write("Invalid job number: " + str(num), 'error')

    return target
def run(job):
    job = id_job(job)
    job_path = os.path.abspath(kremtree.find_common_dir(c.PROJECT_JOBS_DIR))
    job_path = os.path.join(job_path, job, "job.py")

    if not os.path.isfile(job_path):
        log.write("Given job not found", 'error')
        exit(1)

    tasklist = analyse_file(job_path)

    print_task_list(tasklist)
