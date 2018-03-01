import os
from krempack.common import kremtree
from krempack.common import constants as c
from subprocess import check_output
from config import *

supported_terminals = ["gnome-terminal", "xterm", "uxterm", "lxterm"]

def get_terminal():
    terminal = None

    if use_default_terminal:
        terminal = default_terminal
 
    else:
        process = Popen(["echo $COLORTERM"], shell=True,
                                   stdout=PIPE, 
                                   stderr=PIPE)
        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode

        out = out.decode("utf-8")
        print("OUT: " + str(out))
        print("ERR: " + str(err))
        print("RC: " + str(errcode))
        if not errcode:
            for check_term in supported_terminals:
                if check_term in out:
                    terminal = check_term
                    break
    return terminal

def get_terminal_command(terminal):
    term_cmd = None
        
    if terminal == "gnome-terminal":
        term_cmd = "gnome-terminal --geometry " + terminal_size + " -e "
    elif terminal ==  "xterm":
        term_cmd = "xterm -geometry " + terminal_size + " -e "
    elif terminal == "uxterm":
        term_cmd = "uxterm -geometry " + terminal_size + " -e "
    elif terminal == "lxterm":
        term_cmd = "lxterm -geometry " + terminal_size + " -e "
    else:
        print('[ERROR]: Failed to get terminal name. Ensure you are running a terminal supported by the debug-terminal plugin')
    return term_cmd

def try_to_run(terminal, filepath):
    success = False

    if not os.system("which " + terminal + " > /dev/null"):
        success = True

    if success:
        launch_string = '"bash -c \'pandoc ' + filepath + ' | lynx -stdin\'"'
        cmd = str(get_terminal_command(terminal)) + launch_string
        try:
            os.system(cmd)
        except Exception as e:
            print("Failed to launch. Exception raised: " + str(e))

    return success

def display_doc(path):
    doc_path = None

    if ".md" in path:
        doc_path = path
    else:
        for dir in os.listdir(path):
            if ".md" in dir:
                doc_path = os.path.abspath(os.path.join(path, dir))

    if doc_path is None:
        print("[ERROR]: No md file found")
        exit(1)
    else:

        if use_default_terminal:
           if not try_to_run(default_terminal, doc_path):
               print("[ERROR]: Default terminal '" + default_terminal + "' not found.")
               exit(1)
        else:
            success = False
            # Trying different terminals until success
            for term in supported_terminals:
                success = try_to_run(term, doc_path)
                if success:
                    break

            if not success:
                print("[ERROR]: No supported terminals was found")

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

def display_job_doc(job):
    job = id_job(job)
    path = os.path.join(kremtree.find_common_dir(c.PROJECT_JOBS_DIR), job)


    if os.path.isdir(path):
        display_doc(path)
    else:
        print("[ERROR]: Given job not found")
        exit(1)

def id_task(target):
    task_path = kremtree.find_common_dir(c.PROJECT_TASKS_DIR)
    num = -1
    if isinstance(target, int):
        num = target
    elif isinstance(target, str) and target.isdigit():
        num = int(target)

    if not num < 0:
        tasks = kremtree.list_dir(task_path)
        tasks.sort()
        if not num + 1 > len(tasks):
            idx = 0
            for task in tasks:
                if idx == num:
                    print("Task[" + str(num) + "]: " + str(task))
                    target = task
                    break
                idx = idx + 1
        else:
            print("Invalid task number: " + str(num))

    return target

def display_task_doc(task):
    task = id_task(task)
    path = os.path.join(kremtree.find_common_dir(c.PROJECT_TASKS_DIR), task)

    if os.path.isdir(path):
        display_doc(path)
    else:
        print("[ERROR]: Given task not found")
        exit(1)

def display_manual():
    path = check_output(["which", "krem"]).strip()
    path = path[:-5]
    path = os.path.join(path, "docs", "KREM_USER_MANUAL.md")

    if os.path.isfile(path):
        display_doc(path)
    else:
        print("[ERROR]: Unable to find krem/docs/KREM_USER_MANUAL.md")

def display_readme():
    path = check_output(["which", "krem"]).strip()
    path = path[:-5]
    path = os.path.join(path, "README.md")

    if os.path.isfile(path):
        display_doc(path)
    else:
        print("[ERROR]: Unable to find krem/README.md")

def display_file(file):
    path = file

    if os.path.isfile(path):
        display_doc(path)
    else:
        print("[ERROR]: File not found")
