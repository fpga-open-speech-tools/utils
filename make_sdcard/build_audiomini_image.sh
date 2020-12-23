#!/bin/bash

sudo ./make_sdimage.py -f -P audiomini_preloader.bin,num=3,format=raw,size=10M,type=A2, -P ubuntu-base/*,num=2,format=ext3,size=12G -P zImage,soc_system.rbf,audiomini.dtb,u-boot.img,u-boot.scr,num=1,format=vfat,size=2G -s 15G -n audiomini2_image.img -w ./audiomini