#! /bin/bash
# init-config-user.sh

# install steamcmd
mkdir ~/steamcmd; cd ~/steamcmd; wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz; tar -xvzf steamcmd_linux.tar.gz; rm steamcmd_linux.tar.gz;

# install qlds
./steamcmd.sh +login anonymous +force_install_dir /home/qlserver/steamcmd/steamapps/common/qlds/ +app_update 349090 +quit

# make directories that deploy.sh'll complain about later on if they're not there
mkdir /home/qlserver/steamcmd/common/qlds/minqlx-plugins
mkdir /home/qlserver/steamcmd/common/qlds/baseq3/scripts

# DON'T FORGET TO PUT THE LOCALCONFIG TEXT FILES WHERE THEY NEED TO GO

# grab initialise.sh and run
wget https://raw.githubusercontent.com/TomTec-Solutions/QL-Server-Config/master/initialise.sh
dos2unix initialise.sh
chmod +x initialise.sh
./initialise.sh

# should be done now
