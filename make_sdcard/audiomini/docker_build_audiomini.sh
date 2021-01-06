#!/bin/bash 
cp ../frost_usd_card_blueprint.xml ./DistroBlueprint.xml

# Build the Audio Mini Linux Image with Docker
project="build_audiomini_image"

docker build -t $project .
# docker run --name $project --privileged $project 
docker run --entrypoint "/bin/bash" -it --name $project --cap-add=CAP_MKNOD --privileged $project 
docker cp $project:/tmp/audio-mini.img .
docker rm -f $project
docker rmi -f $project
