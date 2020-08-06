#!/bin/bash

# install all of the packages
# https://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file

cp sources.list /etc/apt/


apt update && apt upgrade -y
xargs -a <(awk '! /^ *(#|$)/' packages) -r -- apt -y install 

cp ssh.service /etc/avahi/services
cp hosts /etc/avahi/
cp sshd_config /etc/ssh/

bash <(curl -L https://github.com/balena-io/wifi-connect/raw/master/scripts/raspbian-install.sh)

# setup our root user
# TODO: we really should not be using root for everything
#       we should create a normal user and disable the root account, 
#       or at least give it a strong password...
echo "root:root" | chpasswd

# we're done; exit the chroot
exit

