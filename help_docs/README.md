
# Description

Adds the command "krem help", which quickly displays markdown files such as KREM manual, KREM readme, and job/task help files. 

# Requirements

This plugin supports Linux only, and requires at least one of the following terminals to be installed:

	* gnome-terminal
    * xterm
    * uxterm
    * lxterm

The following packages are required:

	* Pandoc 
    * Lynx   
Installation with apt: _sudo apt-get install pandoc lynx_.
 
# Usage
## Setup
It is here assumed that file is located in _\<krem\_project\>/library/plugins/help\_docs._
It is also assumed that your plugin setup file is _\<krem\_project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.help_docs.help_docs_cli import PluginHelpDocs
```

and add the following to the `setup_cli_plugins` function:

```
def setup_cli_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginHelpDocs)
```
## Add and Display Job/Task Help Files
Add a single _<name>.md_ file to the desired task or job directory.
Example:
	_krem\_project/tasks/task_foo/README.md_

Display the help file by calling _krem help -t task\_foo_ or _krem help -j job\_foo_
