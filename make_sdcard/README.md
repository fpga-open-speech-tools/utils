# Overview
This procedure describes how to create a working FrOST Audio Mini $\mu$SD card image using a [Python generation tool.](https://github.com/robseb/LinuxBootImageFileGenerator) NOTE: This README is a work in progress.
# Prerequisites

## Operating Systems
Linux is recommended.  

## Dependencies
Python3 is required to run the generation script.

# Procedure
1. Clone the [LinuxBootImageFileGenerator](https://github.com/robseb/LinuxBootImageFileGenerator) repository. [TODO: Fork the repo and make edits for fully automated builds]
2. Copy the DistroBlueprint.xml file into the LinuxBootImageFileGenerator directory
3. Copy the following files into the `Image_partitions/Pat_1_vfat` directory
	1. The device tree for the FPGA
	2. The raw binary file for the FPGA design
	3. The Linux kernel
	4. The U-Boot script
	5. The U-Boot image
4. Copy the following file into the `Image_partitions/Pat_3_raw` directory
	1. The the FPGA device's preloader
5. Copy the desired filesystem into the `Image_partitions/Pat_2_ext3` directory
	 1. This can be any filesystem the user desires.  For this procedure, it is assumed that the [build_rootfs.sh](https://github.com/fpga-open-speech-tools/utils/tree/make_sdcard_dev/rootfs) script was used to create an Ubuntu filesystem.
 6. Finally, execute the command `python3 LinuxBootImageFileGenerator.py` and press any key to pass through the prompts.

