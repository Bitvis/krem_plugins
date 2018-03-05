import datetime
import os
import subprocess
import re

from krempack.core import plugin
from krempack.common import kremtree

from . import info_config as config

class PluginJobIntroText(plugin.Plugin):
    name = "job-intro-text"
    default_padding = "{:15}"

    def __init__(self):
        self.job = None
        self.log_file = None
 
    def job_start(self, job):
        self.job = job
        self.log_file = job.log.get_log_file()
        intro_text = []

        if config.add_krem_version:
            intro_text.append(self.get_krem_version())

        if config.add_date:
            intro_text.append(self.get_date())
        
        if config.add_project_name:
            intro_text.append(self.get_project_name())

        if config.add_project_path:
            intro_text.append(self.get_project_path())

        if config.add_job_name:
            intro_text.append(self.get_job_name())

        if config.add_user_name:
            intro_text.append(self.get_user_name())

        if config.add_additional_info:
            for line in config.additional_info:
                intro_text.append(line)

        file = open(self.log_file, 'a')

        for line in intro_text:
            file.write(line + "\n")
            print(line)

        print("")
        file.write("\n")

    def get_krem_version(self):
        version = None
        text = self.default_padding.format("Version:")

        output = subprocess.check_output(["which", "krem"])
        krem_path = output.decode("utf-8").strip()

        file = open(krem_path, 'r')
        for line in file.readlines():
            if "KREM_VERSION" in line:
                match = re.search("\d+.\d+.\d+", line)
                if match:
                    version = match.group(0)

        if version:
            text = text + "KREM v" + version
        else: 
            text = text + "not found"
        
        return text

    def get_date(self):
        text = self.default_padding.format("Date:")
        now = datetime.datetime.now()
        date = {"year": now.year, "month": now.month, "day": now.day}

        implemented_date = []

        for entry in config.date_order:
            implemented_date.append(date[entry])

        text = text + config.date_format.format(implemented_date[0], implemented_date[1], implemented_date[2])

        return text

    def get_project_name(self):
        text = self.default_padding.format("Project:")
        text = text + str(os.path.abspath(kremtree.find_krem_root(".")).split(os.path.sep)[-1])
        return text

    def get_project_path(self):
        text = self.default_padding.format("Project path:")
        text = text + os.path.abspath(kremtree.find_krem_root("."))
        return text

    def get_job_name(self):
        text = self.default_padding.format("Job:")
        text = text + self.job.name
        return text

    def get_user_name(self):
        text = self.default_padding.format("User:")
        user = ""
        if len(config.user_name) > 0:
            user = config.user_name
        else:
            user = os.environ['USER']

        text = text + user

        return text