# Define the Container - Ubuntu 20.04
FROM ubuntu:focal
# Update the Packages
RUN apt-get update
# Install the required packages for the Audio Mini Build Script
RUN apt install \
    # WGET to download the artifcats from S3
    wget \
    # Sudo to run the build script
    sudo \
    # Git to clone the Linux Builder Repo
    git \
    # Python3 to run the Linux Builder Python Script
    python3 \
    # dosfstools installs mkfs.vfat which is used in the image creation
    dosfstools -y 
# Copy the local files into the container
COPY * /tmp/
# Set the working directory to the location of the files
WORKDIR /tmp
# Set the entry point as the Build Audio Mini Script
ENTRYPOINT ["/bin/bash","./build_audiomini_image.sh"]
