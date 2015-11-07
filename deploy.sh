#! /bin/bash
# quake server config/data deploy


# Variables
HOME="/home/qlserver"
QLDS="$HOME/steamcmd/steamapps/common/qlds
BASEQ3="$QLDS/baseq3"


#
#  Downloading the GitHub Repository.
#
cd ~
git clone https://github.com/TomTec-Solutions/QL-Server-Config.git
cd QL-Server-Config

# Running pre-run script.
bash pre-run.sh

#
#  Performing main data move.
# 

# Moving all access files
cd accesses
mv * $BASEQ3/
cd ..

# Moving all configuration files
cd config-files
mv server.txt $BASEQ3/server.cfg
sudo mv supervisord.txt /etc/supervisord.conf
mv workshop.txt $BASEQ3/workshop.txt
cd ..

# Moving all factories
cd factories
mv * $BASEQ3/scripts
cd ..

# Moving all map-pools
cd mappools
mv * $BASEQ3/
cd ..

# Moving all scripts
cd scripts
mv rcon.py $QLDS/rcon.py
mv * $HOME/
cd ..


# Running post-run script
bash post-run.sh

#
#  Removing GitHub Repository.
#
cd ~
rm -rf QL-Server-Config

# Finished.
exit 0