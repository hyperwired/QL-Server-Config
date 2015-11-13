#! /bin/bash
# quake server data deployment initialiser
# created by Thomas Jones on 13/11/15.


# Variables
GITURL="https://github.com/TomTec-Solutions/QL-Server-Config.git"


#
#  Downloading the GitHub Repository and preparing 'deploy.sh'
#
cd ~
rm -rf "QL-Server-Config" # removes failed installs
echo "Downloading the 'QL-Server-Config.git' repository..."
git clone $GITURL > /dev/null
cd QL-Server-Config
cp deploy.sh ~/deploy.sh
chmod +x ~/deploy.sh

#
#  Running 'deploy.sh'
#
bash ~/deploy.sh

rm -rf ~/QL-Server-Config
exit