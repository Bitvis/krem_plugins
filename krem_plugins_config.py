# Plugin logger config

'''
These are the default configurations. Every plugin can overwrite these configurations by defining a
configuration in the same way as below and pass it to the log.write function as below

log.write(text, "info", logger_format=<plugin logger format>)
'''



# Format of log entries from hooks 'pre_task_function_call' and 'post_task_function_call' 
#(passed to task logger)
plugin_logger_tc_format = [ {"property" : "log_level",   "format": "{}".format("[{input}]:"),           "enabled": True},
                            {"property" : "log_entry",   "format": "{}".format("{input}"),              "enabled": True},
                            {"property" : "plugin_name", "format": "{}".format("     [plugin:{input}]"), "enabled": True}]

# Level on task log entries (error, warning, info, debug)
tc_log_level = "debug"

# Format of log entries from hooks 'job_start', 'pre_task_execution', 'job_progress_text', 'post_task_execution' and 'job_end'
#(passed to terminal and execution logger)
plugin_logger_ec_format = [ {"property" : "log_entry",   "format": "{}".format("{input}"),          "enabled": True},
                            {"property" : "plugin_name", "format": "{}".format("     [plugin:{input}]"), "enabled": True},]



# Format of log entries from CLI hooks 
#(passed to terminal only)
plugin_logger_cli_format = [{"property" : "log_level",   "format": "{}".format("[{input}]:"),           "enabled": True},
                            {"property" : "plugin_name", "format": "{:<30}".format("plugin[{input}]:"), "enabled": False},
                            {"property" : "log_entry",   "format": "{}".format("{input}"),              "enabled": True}]

# Level on task log entries (error, warning, info, debug)
cli_log_level = "debug"
