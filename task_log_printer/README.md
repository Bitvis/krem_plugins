
# Description

Adds the command "krem log", which prints the task log of the given job instance to the terminal. 
 
# Usage
## Setup
It is here assumed that file is located in _\<krem\_project\>/library/plugins/task\_log\_printer._
It is also assumed that your plugin setup file is _\<krem\_project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.task_log_printer.task_log_printer import PluginTaskLogPrinter
```

and add the following to the `setup_cli_plugins` function:

```
def setup_cli_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginTaskLogPrinter)
```