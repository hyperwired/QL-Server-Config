#! /bin/bash
# quake server config/data deploy
# created by Thomas Jones on 08/11/15.


# Variables
HOME="/home/qlserver"
QLDS="$HOME/steamcmd/steamapps/common/qlds"
BASEQ3="$QLDS/baseq3"
GITURL="https://github.com/TomTec-Solutions/QL-Server-Config.git"

cd ~

#
#  Downloading the GitHub Repository.
#
echo "Downloading the 'QL-Server-Config.git' repository..."
git clone $GITURL > /dev/null
cd QL-Server-Config

# Running pre-run script.
echo "=== Running pre-run script..."
bash pre-run.sh
echo "=== End of pre-run script."

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
dos2unix $BASEQ3/server.cfg > /dev/null
sudo mv supervisord.txt /etc/supervisord.conf
sudo dos2unix /etc/supervisord.conf > /dev/null
mv workshop.txt $BASEQ3/workshop.txt
dos2unix $BASEQ3/workshop.txt > /dev/null
cd ..

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

#echo "Moving minqlx.zip into place..."
#mv minqlx.zip $QLDS/minqlx.zip

echo "Zipping up minqlx core files and moving them into place..."
rm -f ~/steamcmd/steamapps/common/qlds/minqlx.zip
zip -r ~/steamcmd/steamapps/common/qlds/minqlx.zip minqlx/*

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
echo "=== End of post-run script."

# Finished, cleaning up and exiting.
echo "Deployment complete."
cp deploy.sh ~/deploy.sh; cd ~; rm -rf QL-Server-Config; exit