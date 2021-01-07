#!/bin/bash
# Clone the LinuxBootImageFileGenerator Repo
git clone https://github.com/fpga-open-speech-tools/LinuxBootImageFileGenerator.git

# Copy DistroBlueprint.xml into LinuxBootImageFileGenerator
cp DistroBlueprint.xml LinuxBootImageFileGenerator/;

# Make the Image_partitions/Pat_1_vfat Folder
mkdir -p LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# Check for the Audio Mini DTB
if [ -f soc_system.dtb ]; then
    echo 'Using the local Audio Mini DTB.'
else
    echo 'Downloading the Audio Mini DTB from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/soc_system.dtb
fi
cp soc_system.dtb LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# Check for the Audio Mini Raw Binary File
if [ -f soc_system.rbf ]; then
    echo 'Using the local Audio Mini RBF.'
else
    echo 'Downloading the Audio Mini RBF from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/soc_system.rbf
fi
cp soc_system.rbf LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# Check for the zImage
if [ -f zImage ]; then
    echo 'Using the local zImage.'
else
    echo 'Downloading the zImage from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/common/zImage
fi
cp zImage LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# Check for the Audio Mini uBoot Source
if [ -f u-boot.scr ]; then
    echo 'Using the local Audio Mini uBoot Source.'
else
    echo 'Downloading the Audio Mini uBoot Source from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/u-boot.scr
fi
cp u-boot.scr LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# Check for the Audio Mini uBoot Image
if [ -f u-boot.img ]; then
    echo 'Using the local Audio Mini uBoot Image.'
else
    echo 'Downloading the Audio Mini uBoot Image from S3 Archive'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/u-boot.img
fi
cp u-boot.img LinuxBootImageFileGenerator/Image_partitions/Pat_1_vfat/;

# Make the Image_partitions/Pat_3_raw Folder
mkdir -p LinuxBootImageFileGenerator/Image_partitions/Pat_3_raw;
# Check for the Audio Mini Preloader
if [ -f audiomini_preloader.bin ]; then
    echo 'Using the local Audio Mini Preloader.'
else
    echo 'Downloading the Audio Mini Preloader from S3 Archive.'
    wget https://frost-release.s3-us-west-2.amazonaws.com/linux-images/artifacts/audiomini/audiomini_preloader.bin
fi
cp audiomini_preloader.bin LinuxBootImageFileGenerator/Image_partitions/Pat_3_raw;

# Make the Image_partitions/Pat_2_ext3 Folder
mkdir -p LinuxBootImageFileGenerator/Image_partitions/Pat_2_ext3;
# Check for the Root File System
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

cd LinuxBootImageFileGenerator; 
python3 LinuxBootImageGenerator.py;
mv LinuxDistro*.img audio-mini.img;