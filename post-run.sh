#! /bin/bash
# Post-run script

echo "Making all scripts in '~/' executable..."
chmod +x ~/*.sh

echo "Running 'quakeupdate.sh'..."
bash ~/quakeupdate.sh

exit 0