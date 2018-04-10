
# Description

Separate task log extracts log from tasks.log for given task and writes the log to the tasks output directory.
The log is extracted after the task has finished execution. This means that to watch the task output as it is written, the tasks.log file has be used.



# Usage
It is here assumed that file is located in _\<krem project\>/library\plugins\time\_task\_function_.
It is also assumed that your plugin setup file is _\<krem project\>\_library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.separate_task_log.separate_task_log import PluginSeparateTaskLog
```

and add the following to the `setup_plugins` function:

```
def setup_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginSeparateTaskLog)
    plugin_handler.hooks["post_task_function_call"].append_last_to_execute(PluginSeparateTaskLog)

```

