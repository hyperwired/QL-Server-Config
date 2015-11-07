#! /bin/bash
cd ~

CURRENT_MINQLX_VERSION=$(cat minqlx.version)
LATEST_MINQLX_VERSION="0.0.4a"

if [ $CURRENT_MINQLX_VERSION != $LATEST_MINQLX_VERSION ]; then
    echo "Upgrading minqlx from version $CURRENT_MINQLX_VERSION to $LATEST_MINQLX_VERSION..."
    sudo rm -rf ~/steamcmd/steamapps/common/qlds/minqlx.zip ~/steamcmd/steamapps/common/qlds/minqlx.so > /dev/null
    mkdir temp; cd temp
    wget https://github.com/MinoMino/minqlx/releases/download/v0.0.4a/minqlx_v0.0.4a.tar.gz > /dev/null
    tar xvzf minqlx_v0.0.4a.tar.gz > /dev/null
    cd minqlx_v0.0.4a
    mv minqlx.zip ~/steamcmd/steamapps/common/qlds/minqlx.zip
    mv minqlx.so ~/steamcmd/steamapps/common/qlds/minqlx.so
    cd ~
    rm -rf temp
    echo "0.0.4a" > ~/minqlx.version
else
    echo "minqlx is up-to-date (version $CURRENT_MINQLX_VERSION)."
fi
