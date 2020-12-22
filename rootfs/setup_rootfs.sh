#!/bin/bash

echo 
echo "updating packages..."
echo
apt update && apt upgrade -y

# install all packages in the packages file
# https://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file
echo
echo "installing packages..."
echo
export DEBIAN_FRONTEND=noninteractive
ln -fs /usr/share/zoneinfo/America/Denver /etc/localtime
xargs -a <(awk '! /^ *(#|$)/' packages) -r -- apt -y --no-install-recommends install 

# avahi config files need to be copied after avahi is installed
# mv ssh.service /etc/avahi/services
# mv hosts /etc/avahi/

echo nameserver 8.8.8.8 >> /etc/resolvconf/resolv.conf.d/head
echo nameserver 8.8.4.4 >> /etc/resolvconf/resolv.conf.d/head
resolvconf --enable-updates
resolvconf -u

# Install FrOST Edge
dpkg -i /frost-edge.deb
rm /frost-edge.deb

# Install Python Packages
echo "Install Python Packages:"
echo "   Install Boto3"
pip3 install boto3
echo "   Installing TQDM"
pip3 install tqdm
echo "   Installing Requests"
pip3 install requests

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

