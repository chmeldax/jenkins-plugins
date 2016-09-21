# Jenkins Plugins

Tiny Python package to download Jenkins plugins along with their dependencies (as there is currently no package manager for Jenkins plugins).

# Requirements

* Python 3

# Installing

```bash
make
```

# Testing

```bash
make test
```

# Usage

```bash
source env/bin/activate
python3 jenkins_plugins.py [plugin_name_1 plugin_name_2 ...]
```

# Known issues

* The script downloads only the latest versions of plugins.
* There is no version conflict resolution.
* You'll need to manually update permissions for plugins.

