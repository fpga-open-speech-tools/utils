docker build -t build_rootfs .
docker run --name build_rootfs --privileged build_rootfs 
docker cp build_rootfs:/tmp/rootfs.tar.gz .
docker rm build_rootfs
docker rmi build_rootfs