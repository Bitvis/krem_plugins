import sys
import os

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
import krem_plugins_config as config

    
class PluginLogger():
    log_levels = {"error":0, "warn":1, "info":2, "debug":3}

    def __init__(self, plugin_name, job_log=None):
        self.parent_name = plugin_name
        self.info_list = []
        self.tc_log_level = config.tc_log_level
        self.cli_log_level = config.cli_log_level
        self.job_log = job_log

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

    def process_info(self, info):
        new_text = ""
        if info["enabled"] and info["input"] is not None:
            new_text = info["format"].format(input=info["input"])
        return new_text

    def process_log_entry(self, msg, level):     
        text = ""

        for info in self.info_list:
            info["input"] = None
            if info["property"] == "plugin_name" and level is not None:
                info["input"] = self.parent_name
            elif info["property"] == "log_entry":
                info["input"] = msg
            elif info["property"] == "log_level" and level is not None:
                info["input"] = level.upper()

            text = text + self.process_info(info)
        return text
        
    def write(self, msg, level=None):
        # If in task context, write to task log
        if "krempack.components.native.loggers_native.TaskWriter" in str(sys.stdout):
            if self.check_tc_log_level(level):
                self.info_list = config.plugin_logger_tc_format
                log_text = self.process_log_entry(msg, level)
                print(log_text) #Stdout redirected to task log
 
                if level == 'warn' or level == 'error':
                    if self.job_log is not None:
                        self.info_list = config.plugin_logger_ec_format
                        log_text = self.process_log_entry(msg, level)
                        self.job_log.write(log_text, level)

        # If in job context, write to job log
        elif self.job_log is not None:
            self.info_list = config.plugin_logger_ec_format
            log_text = self.process_log_entry(msg, level)
            self.job_log.write(log_text, level)
    
        # If in cli context, write to terminal
        else:
            if self.check_cli_log_level(level):
                self.info_list = config.plugin_logger_cli_format
                log_text = self.process_log_entry(msg, level)
                print(log_text)

