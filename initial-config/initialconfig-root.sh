#! /bin/bash
# init-config-root.sh

# Update distro and reboot! DO MANUALLY
# sed -i -e 's/wheezy/jessie/g' /etc/apt/sources.list
# apt-get update; apt-get upgrade; apt-get dist-upgrade; apt-get purge $(dpkg -l | awk '/^rc/ { print $2 }'); apt-get autoremove; reboot

# Set the time-zone
dpkg-reconfigure tzdata

# Install dependencies (during sid-repo activation, may need to install binutils if C compiler can't compile anything)
apt-get -y install lib32gcc1 curl nano samba build-essential python-dev python-setuptools python3 unzip dos2unix cron mailutils wget lib32z1 lib32stdc++6 libc6 git python-pip
sudo bash -c "echo \"deb http://ftp.debian.org/debian sid main\" >> /etc/apt/sources.list"; apt-get update; apt-get -y install python3.5 python3.5-dev; sudo sed -i '$ d' /etc/apt/sources.list; apt-get update
wget https://raw.githubusercontent.com/pypa/get-pip/master/get-pip.py; python3.5 get-pip.py
easy_install supervisor
python3.5 -m easy_install pyzmq hiredis
python3.5 -m pip install redis hiredis requests pyzmq python-valve

# Add qlserver user and configure samba shares
useradd -m qlserver; usermod -a -G sudo qlserver; chsh -s /bin/bash qlserver; clear; echo "Enter the password to use for QLserver account:"; passwd qlserver; echo "qlserver ALL = NOPASSWD: ALL" >> /etc/sudoers; /etc/init.d/samba stop; echo -e "\n[homes]\n    comment = Home Directories\n    browseable = yes\n    read only = no\n    writeable = yes\n    create mask = 0755\n    directory mask = 0755" >> /etc/samba/smb.conf; /etc/init.d/samba start; smbpasswd -a qlserver; smbpasswd -a root
