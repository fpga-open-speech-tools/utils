FROM ubuntu:focal
RUN apt-get update
RUN apt install wget sudo git python3 dosfstools -y 
COPY * /tmp/
WORKDIR /tmp
ENTRYPOINT ["/bin/bash","./build_audiomini_image.sh"]
