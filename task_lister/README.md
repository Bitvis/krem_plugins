
# Description

Adds the command argument "krem list --job-tasks <job>", which lists tasks used in target job. 

# Usage
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
