#! /bin/bash
# Pre-run script

# Upgrade minqlx if needed.
bash minqlx-upgrade.sh

# Kill supervisord, so our new config is activated.
sudo killall supervisord

exit 0