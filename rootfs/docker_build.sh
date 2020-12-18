docker build -t build_rootfs .
docker run --name build_rootfs --privileged build_rootfs 
#docker run --name build_rootfs --privileged --entrypoint /bin/bash -it build_rootfs 
docker cp build_rootfs:/tmp/rootfs.tar.gz .
docker rm -f build_rootfs
docker rmi -f build_rootfs
