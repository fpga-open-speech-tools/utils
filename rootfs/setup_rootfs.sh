#!/bin/bash

# TODO: apt keeps complaining about our locale not being set; we should probably set it properly

# add non-free sources so we can install the ralink wifi firmware
cp sources.list /etc/apt/

echo 
echo "updating packages..."
echo
apt update && apt upgrade -y

# install all packages in the packages file
# https://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file
echo
echo "installing packages..."
echo
xargs -a <(awk '! /^ *(#|$)/' packages) -r -- apt -y --no-install-recommends install 

# avahi config files need to be copied after avahi is installed
cp ssh.service /etc/avahi/services
cp hosts /etc/avahi/
cp sshd_config /etc/ssh/

dpkg -i /frost-edge.deb
rm /frost-edge.deb

# install balena-io wifi-connect
yes N | bash <(curl -L https://github.com/balena-io/wifi-connect/raw/master/scripts/raspbian-install.sh)

echo

# install dotnet core runtime
curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin

echo
echo "setting up user account..."
echo
# setup our root user
# TODO: we really should not be using root for everything
#       we should create a normal user and disable the root account, 
#       or at least give it a strong password...
echo "root:root" | chpasswd

# we're done; exit the chroot
echo "done setting up rootfs..."
exit

