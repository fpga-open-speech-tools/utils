# FrOST Root FS

## Key Files
 - `docker_build.sh` Bash script that delegates the build process to docker
 - `build_rootfs.sh` Downloads base image, then prepares the rootfs for set up, and cleans up the rootfs after set up
 - `setup_rootfs.sh` Sets up the rootfs by installing packages and changing adding custom settings
 - `packages` List of packages that will be installed when `setup_rootfs.sh` is run

## Building the Root FS with Docker
1. Install [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
2. Open WSL and Navigate to `[FrOST Repos]\utils\rootfs\`
3. Run `./docker_build.sh`  

The rootfs is output as `rootfs.tar.gz` 
