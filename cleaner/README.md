
# Description

Add KREM command for cleaning output directories

# Usage
It is here assumed that file is located in _\<krem project\>/library/plugins/krem\_plugins/cleaner_.
It is also assumed that your plugin setup file is _\<krem project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.cleaner.cleaner import PluginCleaner
```

and add the following to the `setup_cli_plugins` function:

```
def setup_cli_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginCleaner)
```
