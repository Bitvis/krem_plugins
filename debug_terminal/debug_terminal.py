import os
from krempack.core import plugin
from krempack.common import kremtree
from subprocess import Popen, PIPE
from multiprocessing import Process
from time import sleep

supported_terminals = ["gnome-terminal", "xterm", "uxterm", "lxterm"]
default_terminal = 'gnome-terminal'
use_default_terminal = False


class PluginDebugTerminal(plugin.Plugin):
    name = "debug-terminal"
    process = None

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
            print("OUT: " + str(out))
            print("ERR: " + str(err))
            print("RC: " + str(errcode))
            if not errcode:
                for check_term in supported_terminals:
                    if check_term in out:
                        terminal = check_term
                        break

        return terminal

    def get_terminal_command(self, terminal, log):
        term_cmd = None
        
        if terminal == "gnome-terminal":
            term_cmd = "gnome-terminal -e "
        elif terminal ==  "xterm":
            term_cmd = "xterm -hold -e "
        elif terminal == "uxterm":
            term_cmd = "uxterm -e "
        elif terminal == "lxterm":
            term_cmd = "lxterm -e "
        else:
            log.write('Failed to get terminal name. Ensure you are running a terminal supported by the debug-terminal plugin', 'error')
        return term_cmd

    def tracer(self, log_path, log):
        success = False

        if use_default_terminal:
            success = self.try_to_run(default_terminal, log_path, log)
        else:
            # Trying different terminals until success
            for term in supported_terminals:
                success = self.try_to_run(term, log_path, log)
                if success:
                    break

        if not success:
            log.write("Failed to launch plugin 'debug-terminal'", "error")

    def try_to_run(self, terminal, log_path, log):
        cmd = str(self.get_terminal_command(terminal, log)) + '"tail -f ' + log_path + '"'
        success = True

        try:
            if os.system(cmd):
                success= False
        except Exception as e:
            success = False
 
        return success

    def job_start(self, job):
        task_log_path = os.path.abspath(os.path.join(job.config.get_root_output_path(), job.config.get_task_logger()().get_log_file_name()))

        file = open(task_log_path, 'w')
        file.close()

        try:
            PluginDebugTerminal.process = Process(target=self.tracer, args=(task_log_path,job.log,)) 
            PluginDebugTerminal.process.start()
            job.log.write('Debug terminal started', 'debug')
            sleep(0.5)
        except Exception as e:
            job.log.write('Failed to start debug terminal. Exception raised: ' + str(e), 'error')

    def job_end(self, job):
        if PluginDebugTerminal.process.is_alive():
            try:
                PluginDebugTerminal.process.terminate()
                job.log.write('Debug terminal stopped', 'debug')
            except Exception as e:
                job.log.write('Failed to stop debug terminal. Exception raised: ' + str(e), 'error')
