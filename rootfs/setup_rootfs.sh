#!/bin/bash

# install all of the packages
# https://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file
apt update && apt upgrade -y
xargs -a <(awk '! /^ *(#|$)/' packages) -r -- apt -y install 

# setup our root user
# TODO: we really should not be using root for everything
#       we should create a normal user and disable the root account, 
#       or at least give it a strong password...
echo "root:root" | chpasswd

# enable serial login getty
systemctl enable getty@ttyS0.service

# we're done; exit the chroot
exit

