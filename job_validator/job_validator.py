import os
import re
import sys
from krempack.common import kremtree
from krempack.common import constants as c

sys.path.append(os.path.join("..", os.path.dirname(__file__)))
import job_validator_config

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger


class err():
    function_call = "Incorrect function call: {}"
    syntax_multiple = "Multiple instances of line '{}'"
    syntax_missing = "Missing line '{}'"
    syntax_erroneous_order = "Unexpected order of required lines.\nExpected: {}\nFound: {}"
    arg_not_string = "Unable to validate {}: {}. Argument instead of string."
    run_task_before_start = "Run task function called before {}."
    run_task_after_start = "Run task function called after {}."
    wait_for_no_running_parallels = "wait_for_complete() called with no running parallel tasks"
    missing_wait_for_parallels = "'{}' called with parallel tasks running. Expected wait_for_complete()."
    not_found = "{} '{}' not found"
    missing_task_function = "Task function '{}' not found in '{}'"
    missing_function_argument = "Argument '{}' missing from function call '{}' in '{}'"
    input_arguments_not_expected = "Task function called with arguments, though none was expected."
    missing_arguments = "Task function '{}:{}' expects arguments. None was given."
    unexpected_arguments = "Unexpected arguments to task function '{}:{}'"
    more_arguments_returned  = "Task function '{}:{}' returns more arguments than catched by caller."
    less_arguments_returned = "Caller catches more arguments than returned by task function '{}:{}'"

class Error():
    def __init__(self):
        self.err_list = []
        self.warnings_on = False
        self.log = None

    def set_logger(self, logger):
        self.log = logger

    def print_err(self):
        for entry in self.err_list:
            if not entry["level"] == "warn" or self.warnings_on:
                printline = ""

                lineentry = ""
                if entry["linenr"]:
                    lineentry = "(Line {})".format(entry["linenr"])
                printline = printline + "{}".format(lineentry)
                    
                printline = printline + entry["text"]
            
                self.log.write(printline, entry['level'])

    def set(self, text, level, linenr=None):
        self.err_list.append({"text":text, "level": level, "linenr":linenr})

class SyntaxValidator():
    print_name = "Job script syntax"

    def __init__(self, job_script):
        self.error = Error()
        self.job_script = job_script
        self.job_script_order = None
        self.log = None

    def set_logger(self, logger):
        self.log = logger
        self.error.set_logger(logger)

    def load_config(self):
        self.job_script_order = job_validator_config.job_script_order
        self.error.warnings_on = job_validator_config.job_script_syntax_warnings_on

    def run(self):
        self.load_config()
        passed = True
        line_order = []

        # Check if expected lines exist, and required lines only once
        for line, line_number in self.job_script:
            for expected in self.job_script_order:
                if len(line) > 0 and line in expected["line"]:
                    if expected["found"] and expected["required"]:
                        self.error.set(err.syntax_multiple.format(line), "error", line_number)
                        passed = False
                    else:
                        expected["found"] = True
                        line_order.append(line)

        # Register missing lines
        for expected in self.job_script_order:
            if not expected["found"]:
                self.error.set(err.syntax_missing.format(expected["line"]), "error")
                passed = False
        
        # Check order of lines
        count = 0
        if passed:
            for expected in self.job_script_order:
                if expected["found"]:
                    if expected["line"] not in line_order[count]:
                        passed = False
                    count = count + 1

            if not passed:
                expected_order = []
                for entry in self.job_script_order:
                    expected_order.append(entry["line"])
                self.error.set(err.syntax_erroneous_order.format(expected_order, line_order), "error")
                passed = False

        return passed

class TaskValidator():
    print_name = "Tasks"

    def __init__(self, job_script):
        self.error = Error()
        self.job_script = job_script
        self.tasklist = []
        self.log = None

    def set_logger(self, logger):
        self.log = logger
        self.error.set_logger(logger)

    def compile_task_list(self):
        call_list = []
        task_func = RunTaskValidator(self.job_script)

        for line, line_number in self.job_script:
            if task_func.is_run_task_call(line):
                call_params = task_func.get_call_params(line, line_number)
                if call_params["name"] is not None and call_params["function"] is not None:
                    call_list.append(call_params)

        for call in call_list:
            task_registered = False
            for task in self.tasklist:
                if call["name"] == task["name"] and call["function"] == task["function"]:
                    task_registered = True
                
            if not task_registered and not re.match("^('|\").*('|\")$", call["name"]):
                self.error.set(err.arg_not_string.format("task", call["name"]), "warn", call["line_number"])
                task_registered = True
            elif not task_registered and not re.match("^('|\").*('|\")$", call["function"]):
                self.error.set(err.arg_not_string.format("task function", call["function"]), "warn", call["line_number"])
                task_registered = True

            if not task_registered:
                self.tasklist.append(call)

    def check_task_files(self):
        success = True
        tasks_dir = os.path.abspath(kremtree.find_common_dir(c.PROJECT_TASKS_DIR))
        error_tasks_found = []
        
        for task in self.tasklist:
            task_function_line = ""
            task_path = os.path.join(tasks_dir, task["name"].strip("'").strip('"'))
            task_script_path = os.path.join(task_path, "task.py")

            if not os.path.isdir(task_path) and task["name"] not in error_tasks_found:
                self.error.set(err.not_found.format("Task directory ", task_path), "error")
                success = False
                error_tasks_found.append(task["name"])
            elif not os.path.isfile(task_script_path) and task["name"] not in error_tasks_found:
                self.error.set(err.not_found.format("Task script ", task_script_path), "error")
                success = False
                error_tasks_found.append(task["name"])
            else:
                file = open(task_script_path, "r")
                for line in file.readlines():
                    line = line.strip()
                    
                    if re.match("^(def)", line) and task["function"].strip("'").strip('"') in line:
                        task_function_line = line
            
            if not len(task_function_line) > 0:
                self.error.set(err.missing_task_function.format(task["function"].strip("'").strip('"'), task_script_path), "error")
                success = False
                
                    
        return success

    def check_task_arguments(self):
        success = True
        tasks_dir = os.path.abspath(kremtree.find_common_dir(c.PROJECT_TASKS_DIR))
        call_list = []
        accepted_calls = []
        task_func = RunTaskValidator(self.job_script)

        for line, line_number in self.job_script:
            if task_func.is_run_task_call(line):
                call_params = task_func.get_call_params(line, line_number)
                if call_params["name"] is not None and call_params["function"] is not None:
                    call_list.append(call_params)

        for call in call_list:
            if re.match("^('|\").*('|\")$", call["name"]) and re.match("^('|\").*('|\")$", call["function"]):
                call["name"] = call["name"].strip("'").strip('"')
                call["function"] = call["function"].strip("'").strip('"')
                accepted_calls.append(call)
        
        task_functions_checked = []
        for call in accepted_calls:
            file = None
            parameters = None

            task_path = os.path.join(tasks_dir, call["name"])
            task_script_path = os.path.join(task_path, "task.py")

            task_function = (call["name"], call["function"])
            
            try:
                file = open(task_script_path, "r")
            except Exception as e:
                None
            
            if file:
                for line in file.readlines():
                    line = line.strip()                
                    if re.match("^(def)", line) and call["function"] in line:
                        parameters = re.search("\(.*\)", line).group().strip("(").strip(")").strip().split(",")

            if parameters is not None:
                if not "task" in parameters[0] and task_function not in task_functions_checked:
                    self.error.set(err.missing_function_argument.format("task", call["function"], task_script_path), "error")

                if call["arguments"]:
                    if ("task" in parameters[0] and len(parameters) < 2) or ("task" not in parameters[0] and parameters[0] == ""):
                        self.error.set(err.unexpected_arguments.format(call["name"], call["function"]), "error", call["line_number"])
                        success = False
                if not call["arguments"]:
                    if ("task" in parameters[0] and len(parameters) > 1) or ("task" not in parameters[0] and parameters[0] != ""):
                        self.error.set(err.missing_arguments.format(call["name"], call["function"]), "error", call["line_number"])
                        success = False

            task_functions_checked.append(task_function)

        return success

    def check_return_arguments(self):
        success = True
        tasks_dir = os.path.abspath(kremtree.find_common_dir(c.PROJECT_TASKS_DIR))
        call_list = []
        accepted_calls = []
        task_func = RunTaskValidator(self.job_script)

        for line, line_number in self.job_script:
            if task_func.is_run_task_call(line):
                call_params = task_func.get_call_params(line, line_number)
                if call_params["name"] is not None and call_params["function"] is not None:
                    call_list.append(call_params)

        for call in call_list:
            if re.match("^('|\").*('|\")$", call["name"]) and re.match("^('|\").*('|\")$", call["function"]):
                call["name"] = call["name"].strip("'").strip('"')
                call["function"] = call["function"].strip("'").strip('"')
                accepted_calls.append(call)
        
        for call in accepted_calls:
            if call["return_arguments"] != 0:
                file = None

                task_path = os.path.join(tasks_dir, call["name"])
                task_script_path = os.path.join(task_path, "task.py")
                
                try:
                    file = open(task_script_path, "r")
                except Exception as e:
                    None
                if file:
                    function_found = False
                    for line in file.readlines():
                        line = line.strip() 
                        if re.match("^(def)", line) and call["function"] in line:
                            function_found = True
                        if re.match("return", line):
                            num_return_arguments = line.split(",")
                            if len(num_return_arguments) > call["return_arguments"]:
                                self.error.set(err.more_arguments_returned.format(call["name"], call["function"]), "warn", call["line_number"])
                                
                            elif len(num_return_arguments) < call["return_arguments"]:
                                self.error.set(err.less_arguments_returned.format(call["name"], call["function"]), "error", call["line_number"])
                                success = False
                            break
                            
        return success

    def load_config(self):
        self.error.warnings_on = job_validator_config.check_tasks_warnings_on

    def run(self):
        success = True
        self.load_config()
        self.compile_task_list()
        success = self.check_task_files() and success
        success = self.check_task_arguments() and success
        success = self.check_return_arguments() and success
        return success

class RunTaskValidator():
    print_name = "Run task function calls"

    def __init__(self, job_script):
        self.error = Error()
        self.job_script = job_script
        self.job_start_call = None
        self.job_end_call = None
        self.log = None

    def set_logger(self, logger):
        self.log = logger
        self.error.set_logger(logger)

    def is_run_task_call(self, line):
        task_call = False
        if "run_task_serial(" in line or "run_task_parallel(" in line:
            task_call = True
        return task_call

    def get_call_params(self, line, line_number):
        taskparams = {"call": line, "name": None, "function": None, "arguments": False, "return_arguments": 0, "line_number": line_number}

        match = re.search(r"\((.*),(.*)(,|\))", line, re.M|re.I)
        if match:
            param_list = match.group().strip("(").strip(")").split(",")
            if not '=' in param_list[0]:
                taskparams["name"] = param_list[0].strip()
            if not '=' in param_list[1]:
                taskparams["function"] = param_list[1].strip()

            for idx, param in enumerate(param_list):
                if idx >= 2:
                    try:
                        if "arguments" in param.strip():                         
                            taskparams["arguments"] = True
                            break
                    except Exception:
                        None

            if re.match(".*=.*run_task_", line):
                return_args = line.split("=")[0].strip().split(",")
                taskparams["return_arguments"] = len(return_args)
        return taskparams

    def validate_function_format(self):
        passed = True
        run_task_calls = []
        for line, line_number in self.job_script:
            if self.is_run_task_call(line):
                run_task_calls.append(self.get_call_params(line, line_number))

        for run_task_call in run_task_calls:
            if run_task_call["name"] is None or run_task_call["function"] is None:
                self.error.set(err.function_call.format(run_task_call["call"]), "error", run_task_call["line_number"])
                passed = False

        return passed

    def validate_function_placement(self):
        success = True
        job_start_found = False
        job_end_found = False

        calls_before_start = []
        calls_after_end = []

        for line, line_number in self.job_script:
            if self.job_start_call in line:
                job_start_found = True
            if self.job_end_call in line:
                job_end_found = True

            if self.is_run_task_call(line):
                if not job_start_found:
                    success = False
                    self.error.set(err.run_task_before_start.format(self.job_start_call), "error", line_number)
                if job_end_found:
                    success = False
                    self.error.set(err.run_task_after_start.format(self.job_end_call), "error", line_number)

        return success

    def validate_parallel_tasks(self):
        success = True

        parallel_run_started = False

        for line, line_number in self.job_script:
            if "run_task_parallel" in line:
                parallel_run_started = True

            elif "wait_for_complete" in line and parallel_run_started:
                parallel_run_started = False

            elif "wait_for_complete" in line and not parallel_run_started:
                self.error.set(err.wait_for_no_running_parallels, "error", line_number)
                success = False

            elif parallel_run_started and self.job_end_call in line:
                self.error.set(err.missing_wait_for_parallels.format(self.job_end_call), "error", line_number)
                success = False

            elif parallel_run_started and "run_task_serial(" in line:
                self.error.set(err.missing_wait_for_parallels.format("run_task_serial()"), "error", line_number)
                success = False

            elif parallel_run_started and "get_task_results(" in line:
                self.error.set(err.missing_wait_for_parallels.format("get_task_results()"), "error", line_number)
                success = False

        return success

    def load_config(self):
        self.job_start_call = job_validator_config.job_script_start_line
        self.job_end_call = job_validator_config.job_script_end_line
        self.error.warnings_on = job_validator_config.run_task_function_call_warnings_on

    def run(self):
        success = True
        self.load_config()

        success = self.validate_function_format() and success
        success = self.validate_function_placement() and success
        success = self.validate_parallel_tasks() and success

        return success


class Validator():
    def __init__(self, job_name, job=None):
        self.job_script = []
        self.job_name = self.id_job(job_name)
        self.job_path = self.get_job_path()
        self.validator_list = []
        self.en_validate_syntax = True
        self.en_validate_run_task_calls = True
        self.en_validate_tasks = True
        self.log = PluginLogger("validator", job)

    def get_job_path(self):
        job_path = os.path.abspath(kremtree.find_common_dir(c.PROJECT_JOBS_DIR))
        job_path = os.path.join(job_path, self.job_name, "job.py")

        if not os.path.isfile(job_path):
            self.log.write("Given job does not exist", 'error')
            exit(1)

        return job_path

    def id_job(self, target):
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
                        target = job
                        break
                    idx = idx + 1
            else:
                self.log.write("Invalid job number: " + str(num), 'error')
                exit(1)

        return target

    def compile_job_script(self):
        comment_lines_detect = False
        file = open(self.job_path, 'r')

        line_number = 1
        for line in file.readlines():
            line = line.strip()
            if not comment_lines_detect and "'''" in line:
                comment_lines_detect = True
            elif comment_lines_detect and "'''" in line:
                comment_lines_detect = False

            if not comment_lines_detect:
                if len(line) > 0 and not re.match("#", line) and not re.match("'''", line):
                    self.job_script.append((line, line_number))

            line_number = line_number + 1

        file.close()

    def print_intro(self, validator):
        self.log.write("Checking: " + validator.print_name, 'info')

    def print_errors(self, validator):
        if len(validator.error.err_list) > 0:
            validator.error.print_err()
    def print_end(self, success):
        if success:
            self.log.write("Validation passed", 'info')
        self.log.write("-------------------------------------")


    def run(self):
        self.log.write("Validating job: " + self.job_name, 'info')
        success = True

        if success:
            self.compile_job_script()

            if self.en_validate_syntax:
                self.validator_list.append(SyntaxValidator(self.job_script))
            if self.en_validate_run_task_calls:
                self.validator_list.append(RunTaskValidator(self.job_script))
            if self.en_validate_tasks:
                self.validator_list.append(TaskValidator(self.job_script))       

            for validator in self.validator_list:
                validator.set_logger(self.log)
                self.print_intro(validator)
                success = validator.run() and success
                if len(validator.error.err_list) > 0:                     
                    self.print_errors(validator)
                    
            self.print_end(success)

        return(not success)
