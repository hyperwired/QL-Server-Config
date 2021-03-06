#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# quake server config/data deployment script
# created by Thomas Jones on 08/11/15.


# Variables
HOME="/home/qlserver"
QLDS="$HOME/steamcmd/steamapps/common/qlds"
BASEQ3="$QLDS/baseq3"

cd ~/QL-Server-Config

# Running pre-run script.
echo "=== Running pre-run script..."
bash deploy-pre-run.sh "$@"
echo "=== End of pre-run script."

#
#  Performing main data move.
#

echo "Moving access files into place..."
rm -rf ~/steamcmd/steamapps/common/qlds/baseq3/access*.txt
cd accesses
mv * $BASEQ3/
cd ..

echo "Moving configuration files into place..."
cd config-files
mv server.txt $BASEQ3/server.cfg
dos2unix $BASEQ3/server.cfg > /dev/null
sudo mv supervisord.txt /etc/supervisord.conf
sudo dos2unix /etc/supervisord.conf > /dev/null
cd ..

echo "Moving workshop files into place..."
cd workshop-files
mv workshop* $BASEQ3/
dos2unix $BASEQ3/workshop* > /dev/null
cd ..

echo "Reloading supervisor configuration into memory..."
supervisorctl reread

echo "Moving factories into place..."
cd factories
mv * $BASEQ3/scripts
dos2unix $BASEQ3/scripts/* > /dev/null
cd ..

echo "Moving map-pools into place..."
cd mappools
mv * $BASEQ3/
dos2unix $BASEQ3/mappool* > /dev/null
cd ..

echo "Moving minqlx core python ZIP into place..."
rm -rf ~/steamcmd/steamapps/common/qlds/minqlx.zip
mv minqlx-core/minqlx.zip $QLDS/minqlx.zip

echo "Moving minqlx.so into place..."
mv minqlx-core/minqlx.so $QLDS/minqlx.so

echo "Moving minqlx plugins into place..."
rm -rf ~/steamcmd/steamapps/common/qlds/minqlx-plugins/*
cd minqlx-plugins
mv * $QLDS/minqlx-plugins
cd ..

echo "Moving server scripts into place..."
cd scripts
mv rcon.py $QLDS/rcon.py
mv * $HOME/
chmod +x ~/*.sh
cd ..

echo "Moving run-server scripts into place..."
cd run-server
mv * ~/steamcmd/steamapps/common/qlds/
chmod +x ~/steamcmd/steamapps/common/qlds/*.sh
cd ..

echo "Removing old crontab..."
crontab -r
echo "Loading new crontab..."
cd config-files
dos2unix crontab.txt
crontab crontab.txt
cd ..

# Running post-run script.
echo "=== Running post-run script..."
bash deploy-post-run.sh "$@"
echo "=== End of post-run script."

# Finished, cleaning up and exiting.
echo "Deployment complete."
