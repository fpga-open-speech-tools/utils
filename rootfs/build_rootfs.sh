#!/bin/sh

UBUNTU_VERSION=18.04.3
ROOTFS_ARCHIVE=ubuntu-base-$UBUNTU_VERSION-base-armhf.tar.gz
ROOT_DIR=ubuntu-base

# cleanup any previous rootfs
if [-d $ROOT_DIR]; then
    rm -rf $ROOT_DIR
fi

# download the rootfs
if [-f $ROOTFS_ARCHIVE]; then
    echo "archive already exists; using that one..."
else
    wget http://cdimage.ubuntu.com/ubuntu-base/releases/$UBUNTU_VERSION/release/ubuntu-base-$UBUNTU_VERSION-base-armhf.tar.gz
fi

# extract the rootfs
mkdir $ROOT_DIR
sudo tar -xpf $ROOTFS_ARCHIVE --directory=ubuntu-base

# install qemu-user-static so we can chroot into the armhf rootfs
sudo apt install qemu-user-static
sudo cp /usr/bin/qemu-arm-static $ROOT_DIR/usr/bin/

# copy our resolv.conf into the armhf rootfs so we have internet when we chroot into it
sudo cp /etc/resolv.conf $ROOT_DIR/etc/resolv.conf

# copy our package list into the armhf rootfs so we can install them once we chroot into the rootfs
cp packages $ROOT_DIR/

# chroot into the armhf rootfs
sudo chroot $ROOT_DIR

# install all of the packages
# https://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file
apt update && apt upgrade
xargs -a <(awk '! /^ *(#|$)/' "$packages") -r -- apt install

# setup our root user
# TODO: we really should not be using root for everything
#       we should create a normal user and disable the root account, 
#       or at least give it a strong password...
echo root | passwd --stdin root

# enable serial login getty
systemctl enable getty@ttyS0.service

# we're done! exit the chroot
exit

# clean up after ourselves
rm $ROOTFS_ARCHIVE
