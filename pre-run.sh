#! /bin/bash
# Pre-run script

# Upgrade minqlx if needed.
bash minqlx-upgrade.sh

# Remove all minqlx plugins
rm -rf ~/steamcmd/steamapps/common/qlds/minqlx-plugins/*.py

exit 0