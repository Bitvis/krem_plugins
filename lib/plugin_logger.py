import sys
import os

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
import krem_plugins_config as config

    
class PluginLogger():
    log_levels = {"error":0, "warn":1, "info":2, "debug":3}

    def __init__(self, plugin_name, job_log=None):
        self.plugin_name = plugin_name
        self.logger_format = []
        self.tc_log_level = config.tc_log_level
        self.cli_log_level = config.cli_log_level
        self.job_log = job_log

        # find longest log_level string
        # we can use it to align log entry text
        self.max_log_level_length = 0
        for level_text in self.log_levels:                    
            if len(level_text) > self.max_log_level_length:
                self.max_log_level_length = len(level_text)


    def check_tc_log_level(self, level):
        ret = True
        if level is not None:
            ret = (level in self.log_levels and self.log_levels[level] <= self.log_levels[self.tc_log_level])
        return ret

    def check_cli_log_level(self, level):
        ret = True
        if level is not None:
            ret = (level in self.log_levels and self.log_levels[level] <= self.log_levels[self.cli_log_level])
        return ret

    def process_format(self, format):
        new_text = ""
        if format["enabled"] and format["input"] is not None:
            new_text = format["format"].format(input=format["input"])
        return new_text

    def process_log_entry(self, msg, level):     
        text = ""
        left_align_offset = 0

        for format in self.logger_format:
            format["input"] = None
            if format["property"] == "plugin_name" and level is not None:
                format["input"] = self.plugin_name
            elif format["property"] == "log_entry":
                format["input"] = msg
            elif format["property"] == "log_level" and level is not None:
                format["input"] = level.upper()
                left_align_offset = len(self.process_format(format)) - len(level) + self.max_log_level_length + 1                
                
            text = text + self.process_format(format)
            # this will align next text added to text.            
            text = text.ljust(left_align_offset)
        return text
        
    def write(self, msg, level=None, logger_format=None):
        # If in task context, write to task log
        if "krempack.components.native.loggers_native.TaskWriter" in str(sys.stdout):
            if self.check_tc_log_level(level):
                if (level == 'warn' or level == 'error') and self.job_log is not None:
                    if logger_format is not None:
                        self.logger_format = logger_format
                    else:
                        self.logger_format = config.plugin_logger_ec_format

                    log_text = self.process_log_entry(msg, level)
                    self.job_log.write(log_text, level) #directs printout to terminal, execution log, and task log
                else:
                    if logger_format is not None:
                        self.logger_format = logger_format
                    else:
                        self.logger_format = config.plugin_logger_tc_format

                    log_text = self.process_log_entry(msg, level)
                    print(log_text) #Stdout redirected to task log

        # If in job context, write to job log
        elif self.job_log is not None:
            if logger_format is not None:
                self.logger_format = logger_format
            else:
                self.logger_format = config.plugin_logger_ec_format
            
            
            log_text = self.process_log_entry(msg, level)            
            self.job_log.write(log_text, level)
    
        # If in cli context, write to terminal
        else:
            if self.check_cli_log_level(level):
                if logger_format is not None:
                    self.logger_format = logger_format
                else:
                    self.logger_format = config.plugin_logger_cli_format                
                log_text = self.process_log_entry(msg, level)
                print(log_text)

