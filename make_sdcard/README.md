# Overview
The [make_sdimage.py](https://releases.rocketboards.org/release/2017.10/gsrd/tools/make_sdimage.py) file is a script developed by Altera for the purpose of building an SD card image from scratch.

---
# Prerequisites
## Operating Systems
Linux is recommended for executing this script.  

---
# Procedure
Several files and folders are required in order to build a complete image with this script.  These include 

1. The filesystem for the SoC FPGA
 1. This can be any filesystem the user desires.  For this procedure, it is assumed that the [build_rootfs.sh](https://github.com/fpga-open-speech-tools/utils/tree/make_sdcard_dev/rootfs) script was used to create an Ubuntu filesystem.
2. The the FPGA device's preloader
3. The device tree for the FPGA
4. The raw binary file for the FPGA design
5. The Linux kernel
6. The U-Boot script
7. The U-Boot image

Copy all the relevant files and folders into the directory with the make_sdimage.py script.  Next, build the SD card image using 

```sudo ./make_sdimage.py -f -P <bootloader_image>,num=3,format=raw,size=10M,type=A2 -P <filesystem_folder>/*,num=2,format=ext3,size=8G -P <linux_image>,<FPGA RBF>,<FPGA device tree>,<U-Boot image>,<U-Boot Script>,num=1,format=vfat,size=2G -s 11G -n a10_image.img```

For the Audio Blade, this command would be

```sudo ./make_sdimage.py -f -P uboot_w_dtb-mkpimage.bin,num=3,format=raw,size=10M,type=A2 -P ubuntu-base/*,num=2,format=ext3,size=8G -P zImage,som_system.rbf,som_system.dtb,u-boot.img,u-boot.scr,num=1,format=vfat,size=2G -s 11G -n a10_image.img```

 The build process takes several minutes to complete. Once finished, the image file can be written to an SD card from either Windows using a tool such as Win32DiskImager or in Linux using the `dd` command

`sudo dd if=a10_image.img of=/dev/sd<X> bs=11G` 
where `<X>` is the SD card.  Be very careful when using the `dd` command in Linux as it is very easy to corrupt the host system if the wrong device is targeted.