# FrOST Linux Image Builder
The FrOST Linux Image Builder utility provide a simple way to generate a new uSD Linux Image for the various FrOST Hardware. The build script will check the local system for the required files and download the missing files from the FrOST Release S3 Bucket. More details about the specific builds can be found in the hardware folders.

## Generated Images
 - [Audio Mini](https://frost-release.s3-us-west-2.amazonaws.com/linux-images/audio-mini-image.zip)

## Image Builder Folder Structure
	|-- audiomini                           # Files specific to the Audio Mini
		|-- build_audiomini_image.sh            # Bash Script to build the Audio Mini Linux Image 
		|-- docker_build_audiomini.sh           # Bash Script to build the Audio Mini Image with Docker
		|-- Dockerfile                          # Dockerfile to define the Docker Container
		|-- Jenkinsile                          # Jenkins Build Script
		|-- ReadMe.md                           # Audio Mini Linux Image Build Instructions
	|-- frost_usd_card_blueprint.xml        # The FrOST uSD Card Partition Structure
	|-- README.md                           # Image Builder Read Me


