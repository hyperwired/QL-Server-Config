#! /bin/bash
cd ~

CURRENT_MINQLX_VERSION=$(cat minqlx.version)
LATEST_MINQLX_VERSION="0.0.4a"

if [ $CURRENT_MINQLX_VERSION != $LATEST_MINQLX_VERSION ]; then
    echo "Upgrading minqlx from version $CURRENT_MINQLX_VERSION to $LATEST_MINQLX_VERSION..."
    sudo rm -rf ~/steamcmd/steamapps/common/qlds/minqlx.zip ~/steamcmd/steamapps/common/qlds/minqlx.so
    wget https://github.com/MinoMino/minqlx/releases/download/v0.0.4a/minqlx_v0.0.4a.tar.gz
    tar -xvfz minqlx_v0.0.4a.tar.gz
    cd minqlx_v0.0.4a
    mv minqlx.zip ~/steamcmd/steamapps/common/qlds/minqlx.zip
    mv minqlx.so ~/steamcmd/steamapps/common/qlds/minqlx.so
    cd ..
    rm -rf minqlx_v0.0.0.4a.tar.gz minqlx_v0.0.4a
    echo "0.0.4a" > minqlx.version
else
    echo "minqlx is up-to-date (version $CURRENT_MINQLX_VERSION)."
fi
