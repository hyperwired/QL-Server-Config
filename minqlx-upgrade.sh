#! /bin/bash
cd ~

CURRENT_MINQLX_VERSION=$(cat ~/minqlx.version)
LATEST_MINQLX_VERSION="0.1.0"
LATEST_MINQLX_URL="https://github.com/MinoMino/minqlx/releases/download/v0.1.0/minqlx_v0.1.0.tar.gz"

if [ $CURRENT_MINQLX_VERSION != $LATEST_MINQLX_VERSION ]; then
    echo "Upgrading minqlx from version $CURRENT_MINQLX_VERSION to $LATEST_MINQLX_VERSION..."
sudo rm -rf ~/steamcmd/steamapps/common/qlds/minqlx.so > /dev/null # no longer remove minqlx.zip
    mkdir temp; cd temp
    wget $LATEST_MINQLX_URL > /dev/null
    tar xvzf minqlx_v$LATEST_MINQLX_VERSION.tar.gz
    #mv minqlx.zip ~/steamcmd/steamapps/common/qlds/minqlx.zip # No longer doing this so I can modify it
    mv minqlx.so ~/steamcmd/steamapps/common/qlds/minqlx.so
    cd ~
    rm -rf temp
    echo "0.0.4a" > ~/minqlx.version
    echo "minqlx is now up-to-date (version $LATEST_MINQLX_VERSION)."
else
    echo "minqlx is up-to-date (version $CURRENT_MINQLX_VERSION)."
fi