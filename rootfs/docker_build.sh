# Verify the EoL Characters - Frost Utils: Issue #22
dos2unix build_rootfs.sh;
dos2unix setup_rootfs.sh;

# Build the FrOST Root FS with Docker
docker build -t build_rootfs .
docker run --name build_rootfs --privileged build_rootfs 
docker cp build_rootfs:/tmp/rootfs.tar.gz .
docker rm -f build_rootfs
docker rmi -f build_rootfs
