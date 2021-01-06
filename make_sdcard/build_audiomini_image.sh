#!/bin/bash
# 1.0 - Clone the LinuxBootImageFileGenerator Repo
if [ -d LinuxBootImageFileGenerator ]; then
    echo 'Using local Linux Boot Image File Generator'
else
    echo 'Cloning Linux Boot Image File Generator from https://github.com/robseb/LinuxBootImageFileGenerator'
    git clone https://github.com/robseb/LinuxBootImageFileGenerator.git
fi

# 3.0 - Copy DistroBlueprint.xml into LinuxBootImageFileGenerator
if [ -f LinuxBootImageFileGenerator/DistroBlueprint.xml ]; then
    echo 'Using local DistroBlueprint.xml in the LinuxBootImageFileGenerator Directory'
else
    echo 'Copying DistroBlueprint.xml into LinuxBootImageFileGenerator'
    cp DistroBlueprint.xml LinuxBootImageFileGenerator/;
fi

# 4.0 - Make the Image_partitions/Pat_1_vfat Folder
mkdir -p LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;
# 4.1 - Check for the Audio Mini DTB
if [ -f soc_system.dtb ]; then
    echo 'Using the local Audio Mini DTB.'
else
    echo 'Downloading the Audio Mini DTB from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/soc_system.dtb
fi
cp soc_system.dtb LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# 4.2 - Check for the Audio Mini Raw Binary File
if [ -f soc_system.rbf ]; then
    echo 'Using the local Audio Mini RBF.'
else
    echo 'Downloading the Audio Mini RBF from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/soc_system.rbf
fi
cp soc_system.rbf LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# 4.3 - Check for the zImage
if [ -f zImage ]; then
    echo 'Using the local zImage.'
else
    echo 'Downloading the zImage from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/common/zImage
fi
cp zImage LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# 4.4 - Check for the Audio Mini uBoot Source
if [ -f u-boot.scr ]; then
    echo 'Using the local Audio Mini uBoot Source.'
else
    echo 'Downloading the Audio Mini uBoot Source from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/u-boot.scr
fi
cp u-boot.scr LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# 4.5 - Check for the Audio Mini uBoot Image
if [ -f u-boot.img ]; then
    echo 'Using the local Audio Mini uBoot Image.'
else
    echo 'Downloading the Audio Mini uBoot Image from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/u-boot.img
fi
cp u-boot.img LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# 5.0 - Make the Image_partitions/Pat_3_raw Folder
mkdir -p LinuxBootImageFileGenerator/Image_partitions/Pat_3_raw;
# 5.1 - Check for the Audio Mini Preloader
if [ -f audiomini_preloader.bin ]; then
    echo 'Using the local Audio Mini Preloader.'
else
    echo 'Downloading the Audio Mini Preloader from S3 Archive.'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/audiomini_preloader.bin
fi
cp audiomini_preloader.bin LinuxBootImageFileGenerator/Image_partitions/Pat_3_raw;

# 6.0 - Make the Image_partitions/Pat_2_ext3 Folder
mkdir -p LinuxBootImageFileGenerator/Image_partitions/Pat_2_ext3;
# 6.1 - Check for the Root File System
if [ -d ubuntu-base ]; then
    echo 'Using the local extracted file system - ubuntu-base.'
else
    if [ -f frost_rootfs.tar.gz ]; then
        echo 'Using the local Root File System.'
        tar -xhzvf frost_rootfs.tar.gz; 
    else
        echo 'Downloading the FrOST Root File System from S3 Archive.'
        wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/common/frost_rootfs.tar.gz
        tar -xhzvf frost_rootfs.tar.gz;
    fi
fi
echo "Copying Root File System to LinuxBootImageFileGenerator/Image_partitions/Pat_2_ext3"
mv ubuntu-base/* LinuxBootImageFileGenerator/Image_partitions/Pat_2_ext3;

cd LinuxBootImageFileGenerator; python3 LinuxBootImageGenerator.py