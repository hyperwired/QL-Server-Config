#! /bin/bash
# quake server data deployment initialiser
# created by Thomas Jones on 13/11/15.


# Variables
GITURL="https://github.com/TomTec-Solutions/QL-Server-Config.git"


#
#  Downloading the GitHub Repository and preparing 'deploy.sh'
#
echo "Initialiser has started."
cd ~
echo "Changed PWD to ~."
rm -rf "QL-Server-Config" # removes failed installs
echo "Downloading the 'QL-Server-Config.git' repository..."
git clone $GITURL > /dev/null
cd QL-Server-Config
cp deploy.sh ~/deploy.sh
chmod +x ~/deploy.sh


#
#  Running 'deploy.sh'
#
echo "'deploy.sh' has arrived. Executing."
bash ~/deploy.sh
echo "'deploy.sh' has left. Exiting."

cp -f initialise.sh ~; cd ~; rm -rf ~/QL-Server-Config
exit