FROM ubuntu:focal
RUN apt-get update
RUN apt install wget sudo curl -y 
COPY * /tmp/
WORKDIR /tmp
ENTRYPOINT ["/bin/bash","./build_rootfs.sh"]