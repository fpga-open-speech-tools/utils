FROM ubuntu:focal
RUN apt-get update
RUN apt install wget sudo -y 
COPY * /tmp/
WORKDIR /tmp
ENTRYPOINT ["/bin/bash","./build_audiomini_image.sh"]