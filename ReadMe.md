# Utilities
FrOST Utilities

## Folder Structure
    |-- frost_edge                      # Frost Edge Packager
        |-- packaging                       # Packaging Files
            |-- debian                          # Debian Packaging Files
            |-- scripts                         # Frost Edge Scripts
                |-- frost_edge.service              # Frost Edge Service that calls frost_edge.sh on boot
                |-- frost_edge.sh                   # Bash Script that starts the web app and node server
            |-- makefile                        # Makefile to build the package
        |-- Jenkinsfile                     # Jenkins File to build the package
        |-- Install.md                      # Installation Steps

    |-- json                            # MATLAB Functions to Read and Write JSON Files
        |-- readjson.m
        |-- writejson.m

    |-- power_controller                # Audio Blade Arduino Power Controller
        |--power_control.ino                # Arduino Code to turn the Audio Blade on and off with a power button

    |-- runtime_config                  # Runtime Configuration Scripts
        |-- aws_overlay_installer.py
        |-- awsdownloader.py
        |-- drivermgr
        |-- overlaymgr
    
    |-- s3                              # FrOST S3 CloudFormation Template Files
        |-- README.md                       # Read Me Guide for using the FrOST S3 CloudFormation Template
        |-- s3-template.json                # FrOST S3 CloudFormation Template
    
    |-- .gitattributes                  # Git Attributes File
    |-- .gitignore                      # Git Ignore File
    |-- LICENSE                         # MIT LICENSE File
    |-- README.md                       # This file