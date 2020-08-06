#!/bin/bash

UBUNTU_VERSION=18.04.3
ROOTFS_ARCHIVE=ubuntu-base-$UBUNTU_VERSION-base-armhf.tar.gz
ROOT_DIR=ubuntu-base

# cleanup any previous rootfs
if [ -d $ROOT_DIR ]; then
    sudo rm -rf $ROOT_DIR
fi

# download the rootfs
if [ -f $ROOTFS_ARCHIVE ]; then
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
cp sources.list $ROOT_DIR/
cp ssh.service $ROOT_DIR/
cp hosts $ROOT_DIR/
cp sshd_config $ROOT_DIR/

# mount stuff in the armhf rootfs
sudo mount -t proc /proc $ROOT_DIR/proc
sudo mount -t sysfs /sys $ROOT_DIR/sys
sudo mount -B /dev $ROOT_DIR/dev
sudo mount -B /dev/pts $ROOT_DIR/dev/pts

# copy the setup script into the armhf rootfs
cp setup_rootfs.sh $ROOT_DIR/

# chroot into the armhf rootfs and do the setup
sudo chroot $ROOT_DIR ./setup_rootfs.sh

# unmount directories in the armhf rootfs
sudo umount -l $ROOT_DIR/dev/pts
sudo umount -l $ROOT_DIR/dev
sudo umount -l $ROOT_DIR/proc
sudo umount -l $ROOT_DIR/sys

# clean up after ourselves
rm $ROOTFS_ARCHIVE

# package up the rootfs
sudo tar -czf rootfs.tar.gz $ROOT_DIR
