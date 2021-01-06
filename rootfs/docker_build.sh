#!/bin/bash 

# Build the FrOST Root FS with Docker
docker build -t build_rootfs .
docker run --name build_rootfs --privileged build_rootfs 
docker cp build_rootfs:/tmp/frost_rootfs.tar.gz .
docker rm -f build_rootfs
docker rmi -f build_rootfs
