# Audio Mini Linux Image Builder
The Audio Mini Linux Image Builder generates the complete Audio Mini uSD Card Image using Docker and the [Linux Boot Image File Generator](https://github.com/fpga-open-speech-tools/LinuxBootImageFileGenerator)

## Key Files
- `build_audiomini_image.sh` - The Audio Mini Image Build Script
    - Checks for and downloads the required files from the FrOST Release S3 Bucket
    - Runs the Linux Boot Image File Generator Python Script
- `docker_build_audiomini.sh` - The Docker Build Script
    - Copies the `frost_usd_card_blueprint.xml` into the current folder
    - Runs the Docker Container
- `Dockerfile`
    - Defines the Docker Container
    - Copies all of the files from the current folder in the Docker Container
    - Run `build_audiomini_image.sh`
- `Jenkinsfile`
    - Automation of the build process using Jenkins

## Building the Audio Mini Linux Image with Docker
1. Install [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
2. Open Windows Subsystem for Linux and Navigate to `[FrOST Repos]\utils\image_builder\audiomini`
3. Make the Docker Build Script executable by running
    - `chmod +x docker_build_audiomini.sh`
4. Run the Docker Build - Audio Mini Bash Script with
    - `./docker_build_audiomini.sh`