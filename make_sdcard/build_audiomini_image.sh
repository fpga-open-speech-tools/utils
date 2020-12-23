#!/bin/bash

# Check for the Audio Mini Preloader
if [ -f audiomini_preloader.bin ]; then
    echo 'Using the local Audio Mini Preloader.'
else
    echo 'Downloading the Audio Mini Preloader from S3 Archive.'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/audiomini_preloader.bin
fi

# Check for the Root File System
if [ -d ubuntu-base ]; then
    echo 'Using the local extracted file system - ubuntu-base.'
else
    if [ -f frost_rootfs.tar.gz ]; then
        echo 'Using the local Root File System.'
        tar -hxvf frost_rootfs.tar.gz
    else
        echo 'Downloading the FrOST Root File System from S3 Archive.'
        wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/common/frost_rootfs.tar.gz
        tar -xhvf frost_rootfs.tar.gz
    fi
fi

# Check for the zImage
if [ -f zImage ]; then
    echo 'Using the local zImage.'
else
    echo 'Downloading the zImage from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/common/zImage
fi

# Check for the Audio Mini RBF
if [ -f soc_system.rbf ]; then
    echo 'Using the local Audio Mini RBF.'
else
    echo 'Downloading the Audio Mini RBF from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/soc_system.rbf
fi

# Check for the Audio Mini DTB
if [ -f soc_system.dtb ]; then
    echo 'Using the local Audio Mini DTB.'
else
    echo 'Downloading the Audio Mini DTB from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/soc_system.dtb
fi

# Check for the Audio Mini uBoot Image
if [ -f u-boot.img ]; then
    echo 'Using the local Audio Mini uBoot Image.'
else
    echo 'Downloading the Audio Mini uBoot Image from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/u-boot.img
fi

# Check for the Audio Mini uBoot Source
if [ -f u-boot.scr ]; then
    echo 'Using the local Audio Mini uBoot Source.'
else
    echo 'Downloading the Audio Mini uBoot Source from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/u-boot.scr
fi

sudo ./make_sdimage.py -f -P audiomini_preloader.bin,num=3,format=raw,size=10M,type=A2, -P ubuntu-base/*,num=2,format=ext3,size=12G -P zImage,soc_system.rbf,soc_system.dtb,u-boot.img,u-boot.scr,num=1,format=vfat,size=2G -s 15G -n audiomini.img