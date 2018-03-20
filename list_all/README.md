
# Description

Adds the command argument "krem list --all", which lists all jobs and tasks available into the project. 

# Usage
## Setup
It is here assumed that file is located in _\<krem\_project\>/library/plugins/list\_all._
It is also assumed that your plugin setup file is _\<krem\_project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.list_all.list_all_cli import PluginListAll
```

and add the following to the `setup_cli_plugins` function:

```
def setup_cli_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginListAll)
```
## The list
When the command is executed a list of all jobs and tasks with the index number, is displayed in the terminal. 
