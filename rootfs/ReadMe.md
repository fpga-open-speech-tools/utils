# FrOST Root FS

## Key Files
 - `docker_build.sh`
 - `build_rootfs.sh`
 - `setup_rootfs.sh`
 - `packages`

## Building the Root FS with Docker
1. Install [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
2. Open WSL and Navigate to `[FrOST Repos]\utils\rootfs\`
3. Run `dos2unix build_rootfs.sh`
4. Run `./docker_build.sh`