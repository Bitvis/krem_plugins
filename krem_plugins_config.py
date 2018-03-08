# Plugin logger config

# Format of log entries in task context (passed to task logger)
plugin_logger_tc_format = [ {"name" : "log_level",   "padding": None, "encapsulation": "[{}]:",       "enabled": True},
                            {"name" : "plugin_name", "padding": 30,   "encapsulation": "plugin[{}]:", "enabled": True},
                            {"name" : "log_entry",   "padding": None, "encapsulation": None,          "enabled": True}]

# Level on task log entries (error, warning, info, debug)
tc_log_level = "info"

# Format of log entries in job context (passed to execution logger)
plugin_logger_ec_format = [ {"name" : "plugin_name", "padding": 30,   "encapsulation": "plugin[{}]:", "enabled": True},
                            {"name" : "log_entry",   "padding": None, "encapsulation": None,          "enabled": True}]



# Format of log entries in CLI context (passed to terminal)
plugin_logger_cli_format = [{"name" : "log_level",   "padding": None, "encapsulation": "[{}]:",       "enabled": True},
                            {"name" : "plugin_name", "padding": 30,   "encapsulation": "plugin[{}]:", "enabled": True},
                            {"name" : "log_entry",   "padding": None, "encapsulation": None,          "enabled": True}]

# Level on task log entries (error, warning, info, debug)
cli_log_level = "info"