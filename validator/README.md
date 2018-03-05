
# Description

Validate job script and tasks used in target job

# Usage
## Setup
It is here assumed that file is located in _\<krem project\>/library/plugins/krem\_plugins/validator_.
It is also assumed that your plugin setup file is _\<krem project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.validator.validator import PluginValidator
```

and add the following to the `setup_cli_plugins` function:

```
def setup_cli_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginValidator)
```

## Validation
The validator checks the following potential issues:

* Required code lines
* Calls to run_task functions: 
	* Calls are made within job.start() and job.end()
	* Calls are made with required input parameters
	* Correct use of job.wait_for_complete() when running parallel tasks
* Tasks used in job:
	* Specified tasks exist
	* Specified task functions exist
	* Specified task functions take the required argument input "task"
	* Correct argument input to given task function (checks only if arguments are provided to task function that require arguments, or if arguments are wrongfully provided to task functions that do not accept arguments. Argument types and amount of arguments is ignored)
	* If caller catches returned arguments, it catches the correct amount of arguments as defined by the target task function
