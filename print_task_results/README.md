
# Description

Prints task result to progress in terminal when task has completed.

For parallel tasks, the printout occurs when all the parallel tasks have completed.

# Usage
It is here assumed that file is located in _\<krem project\>/library\plugins\time\_task\_function_.
It is also assumed that your plugin setup file is _\<krem project\>\_library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugifrom library.plugins.krem_plugins.print_task_results.print_task_results import PluginPrintTaskResults
```

and add the following to the `setup_plugins` function:

```
def setup_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginPrintTaskResults)
```

