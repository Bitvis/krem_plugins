
# Description

Opens new terminal window at job start. Task log is streamed to the new terminal window.

# Requirements

This plugin supports Linux only, and requires at least one of the following terminals to be installed:

	* gnome-terminal
    * xterm
    * uxterm
    * lxterm

# Usage
It is here assumed that file is located in _\<krem project\>/library/plugins/krem\_plugins/debug\_terminal_.
It is also assumed that your plugin setup file is _\<krem project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.debug_terminal.debug_terminal import PluginDebugTerminal
```

and add the following to the `setup_plugins` function:

```
def setup_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginDebugTerminal)
```
