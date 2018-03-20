
# Syntax validator config
job_script_syntax_warnings_on = False
run_task_function_call_warnings_on = True
check_tasks_warnings_on = True


job_script_import_line = "from krempack.core import kjob"
job_script_main_line = "if __name__ == '__main__':"
job_script_init_line = "job = kjob.Job(__file__, rc)"
job_script_start_line = "job.start()"
job_script_end_line = "job.end()"

# Expected code lines to be found in job script, in the expected order.
job_script_order = [{"line": job_script_import_line, "found": False, "required": True, "err_addon": ""},
                    {"line": job_script_main_line, "found": False, "required": True, "err_addon": ""},
                    {"line": job_script_init_line, "found": False, "required": True, "err_addon": ""},
                    {"line": job_script_start_line, "found": False, "required": True, "err_addon": ""},
                    {"line": job_script_end_line, "found": False, "required": True, "err_addon": ""}
                    ]