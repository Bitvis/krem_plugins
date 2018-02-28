
# Description

Adds the command argument "krem list --job-tasks <job>", which lists tasks used in target job. 

# Usage
## Setup
It is here assumed that file is located in _\<krem\_project\>/library/plugins/task\_lister._
It is also assumed that your plugin setup file is _\<krem\_project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.task_lister.task_lister import PluginTaskLister
```

and add the following to the `setup_cli_plugins` function:

```
def setup_cli_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginTaskLister)
```
## The list
When the command is executed a list of tasks, with assigned task function, is displayed in the terminal. 

The task list presents a task with a given function only once, regardless of how many times it is being used in the job.
There is also no indication of execution order.

The prefix '*' informs that a variable has been used as input to the run_task function call. For tasks/functions printed
with this prefix it is the variable name, NOT the task/function name, which is displayed in the list.
