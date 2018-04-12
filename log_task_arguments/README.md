
# Description

Log task arguments logs arguments, passed to task functions, to tasks.log. 


# Usage
It is here assumed that file is located in _\<krem project\>/library\plugins\time\_task\_function_.
It is also assumed that your plugin setup file is _\<krem project\>\_library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.log_task_arguments.log_task_arguments import PluginLogTaskArguments
```

and add the following to the `setup_plugins` function:

```
def setup_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginLogTaskArguments)        

```

