import os
import sys
from krempack.core import plugin
from krempack.common import kremtree
from subprocess import Popen, PIPE
import subprocess
from multiprocessing import Process
from time import sleep

pluginspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pluginspath)
from lib.plugin_logger import PluginLogger

supported_terminals = ["gnome-terminal", "xterm", "uxterm", "lxterm"]
default_terminal = 'gnome-terminal'
use_default_terminal = False


class PluginTaskTasksLogTerminal(plugin.Plugin):
    name = "Task tasks log terminal"
    process = None

    def __init__(self):
        self.log = None

    def get_terminal(self):
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
            
            if not errcode:
                for check_term in supported_terminals:
                    if check_term in out:
                        terminal = check_term
                        break

        return terminal

    def get_terminal_command(self, terminal, job):
        term_cmd = None
        
        if terminal == "gnome-terminal":
            term_cmd = "gnome-termina l -e "
        elif terminal ==  "xterm":
            term_cmd = "xterm -hold -e "
        elif terminal == "uxterm":
            term_cmd = "uxterm -e "
        elif terminal == "lxterm":
            term_cmd = "lxterm -e "
        else:
            self.log.write("Failed to get terminal name. Ensure you are running a terminal supported by the plugin '{}'".format(PluginTaskTasksLogTerminal.name), 'error')
        return term_cmd

    def tracer(self, log_path, job):
        success = False

        if use_default_terminal:
            success = self.try_to_run(default_terminal, log_path, job)
        else:
            # Trying different terminals until success
            for term in supported_terminals:
                success = self.try_to_run(term, log_path, job)
                if success:
                    break

        if not success:            
            self.log.write("Failed to launch plugin '{}'".format(PluginTaskTasksLogTerminal.name), "error")

    def try_to_run(self, terminal, log_path, job):
        cmd = str(self.get_terminal_command(terminal, job)) + '"tail -f ' + log_path + '"'
        success = False

        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            # the above command execution returned 0, other wise we get an exception below
            success = True
        except subprocess.CalledProcessError as e:
            success = False
        except Exception:
            success = False
        return success

    def job_start(self, job):
        self.log = PluginLogger(self.name, job.log)
        task_log_path = os.path.abspath(os.path.join(job.config.get_root_output_path(), job.config.get_task_logger()().get_log_file_name()))

        file = open(task_log_path, 'w')
        file.close()

        try:
            PluginTaskTasksLogTerminal.process = Process(target=self.tracer, args=(task_log_path,job,)) 
            PluginTaskTasksLogTerminal.process.start()
            self.log.write("Plugin '{}' started".format(PluginTaskTasksLogTerminal.name), 'debug')
            sleep(0.5)
        except Exception as e:
            self.log.write("Failed to start plugin '{}' plugin. Exception raised: ".format(PluginTaskTasksLogTerminal.name) + str(e), 'error')

    def job_end(self, job):
        if PluginTaskTasksLogTerminal.process.is_alive():
            try:
                PluginTaskTasksLogTerminal.process.terminate()
                self.log.write("Plugin '{}' stopped".format(PluginTaskTasksLogTerminal.name), 'debug')
            except Exception as e:
                self.log.write("Failed to stop plugin '{}'. Exception raised: ".format(PluginTaskTasksLogTerminal.name) + str(e), 'error')
