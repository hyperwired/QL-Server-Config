#! /bin/bash
# quake server config/data deploy


# Variables
HOME="/home/qlserver"
QLDS="$HOME/steamcmd/steamapps/common/qlds"
BASEQ3="$QLDS/baseq3"


#
#  Downloading the GitHub Repository.
#
cd ~
git clone https://github.com/TomTec-Solutions/QL-Server-Config.git > /dev/null
cd QL-Server-Config

# Running pre-run script.
echo "=== Running pre-run script..."
bash pre-run.sh
echo "=== End of pre-run script..."

#
#  Performing main data move.
# 

echo "Moving access files into place..."
cd accesses
mv * $BASEQ3/
cd ..

echo "Moving configuration files into place..."
cd config-files
mv server.txt $BASEQ3/server.cfg
sudo mv supervisord.txt /etc/supervisord.conf
mv workshop.txt $BASEQ3/workshop.txt
cd ..

echo "Moving factories into place..."
cd factories
mv * $BASEQ3/scripts
cd ..

echo "Moving map-pools into place..."
cd mappools
mv * $BASEQ3/
cd ..

echo "Moving minqlx plugins into place..."
cd plugins
mv * $QLDS/minqlx-plugins
cd ..

echo "Moving server scripts into place..."
cd scripts
mv rcon.py $QLDS/rcon.py
mv * $HOME/
cd ..


# Running post-run script.
echo "=== Running post-run script..."
bash post-run.sh
echo "=== End of post-run script..."

# Finished, cleaning up and exiting.
echo "Deployment complete."
cp deploy.sh ~/deploy.sh; cd ~; rm -rf QL-Server-Config; exit