#!/bin/bash 
cp ../frost_usd_card_blueprint.xml ./DistroBlueprint.xml

# Build the Audio Mini Linux Image with Docker
project="build_audiomini_image"

docker build -t $project .
docker run -v /dev:/dev --name $project --privileged $project 
docker cp $project:/tmp/LinuxBootImageFileGenerator/audio-mini.img .
docker rm -f $project
docker rmi -f $project
