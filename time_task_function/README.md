
# Description

Measures time it takes to execute a task function.

Time is printed to tasks.log during job execution.

# Usage
It is here assumed that file is located in _\<krem project\>/library\plugins\time\_task\_function_.
It is also assumed that your plugin setup file is _\<krem project\>\_library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.time_task_function.time_task_function import PluginTimeTaskFunction
```

and add the following to the `setup_plugins` function:

```
def setup_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginTimeTaskFunction)

    plugin_handler.hooks["pre_task_function_call"].append_last_to_execute(PluginTimeTaskFunction)
    plugin_handler.hooks["post_task_function_call"].append_first_to_execute(PluginTimeTaskFunction)
```

The last two lines makes sure that the _pre_task_function_call_ and _post_task_function_call_ hook functions
implemented in the plugin will be executed just before and just after the task function. This is important
to ensure that the time measurement is as accurate as possible when there are other plugins
implementing the same hooks.
