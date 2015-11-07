#! /bin/bash
# Post-run script

echo "Making all scripts in '~/' executable..."
chmod +x ~/*.sh

echo "Zipping up minqlx core files and putting them in place..."
rm -f ~/steamcmd/steamapps/common/qlds/minqlx.zip
zip -r ~/steamcmd/steamapps/common/qlds/minqlx.zip minqlx.core

exit 0