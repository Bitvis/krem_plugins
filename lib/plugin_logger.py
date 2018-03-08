import sys
import os

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
import krem_plugins_config as config

    
class PluginLogger():
    log_levels = {"error":0, "warn":1, "info":2, "debug":3}

    def __init__(self, plugin_name):
        self.parent_name = plugin_name
        self.info_list = []
        self.tc_log_level = config.tc_log_level
        self.cli_log_level = config.cli_log_level

    def check_tc_log_level(self, level):
        return (level in self.log_levels and self.log_levels[level] <= self.log_levels[self.tc_log_level])

    def check_cli_log_level(self, level):
        return (level in self.log_levels and self.log_levels[level] <= self.log_levels[self.cli_log_level])

    def process_info(self, info):
        new_text = ""
        if info["enabled"] and info["input"] is not None:
            new_text = info["input"]
            new_text_format = "{}"

            if info["encapsulation"] is not None:
                new_text = info["encapsulation"].format(info["input"])

            if info["padding"] is not None:
                new_text_format = "{:<" + str(info["padding"]) + "}"

            new_text = new_text_format.format(new_text)
        return new_text

    def process_log_entry(self, msg, level, task=None, job=None):     
        text = ""

        for info in self.info_list:
            if info["name"] == "plugin_name":
                info["input"] = self.parent_name
            elif info["name"] == "log_entry":
                info["input"] = msg
            elif info["name"] == "log_level":
                info["input"] = level.upper()

            text = text + self.process_info(info)
        return text
        
    def write(self, msg, level, job=None, task=None):
        # If in task context, write to task log
        if "krempack.components.native.loggers_native.TaskWriter" in str(sys.stdout):
            if self.check_tc_log_level(level):
                self.info_list = config.plugin_logger_tc_format
                log_text = self.process_log_entry(msg, level, task, job)
                print(log_text) #Stdout redirected to task log

        # If in job context, write to job log
        elif job is not None:
            self.info_list = config.plugin_logger_ec_format
            log_text = self.process_log_entry(msg, level, task, job)
            job.log.write(log_text, level)
    
        # If in cli context, write to terminal
        else:
            if self.check_cli_log_level(level):
                self.info_list = config.plugin_logger_cli_format
                log_text = self.process_log_entry(msg, level, task, job)
                print(log_text)

