
# Description

Print additional info to terminal and execution.log when running a job. Additional info includes KREM version, project name, date, etc...
See info.config.py for how to modify the output.

# Usage
It is here assumed that file is located in _\<krem project\>/library/plugins/krem\_plugins/job\_intro\_text_.
It is also assumed that your plugin setup file is _\<krem project\>/library/setup.py_.

Import the plugin in _setup.py_

```
from library.plugins.krem_plugins.job_intro_text.job_intro_text import PluginJobIntroText
```

and add the following to the `setup_plugins` function:

```
def setup_plugins(plugin_handler):

    plugin_handler.register_plugin(PluginJobIntroText)
```
