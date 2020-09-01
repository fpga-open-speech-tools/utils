#!/usr/bin/python3
"""
Download and install FPGA overlays from AWS.

This is a wrapper script that calls the awsdownloader, overlaymgr, and drivermgr
in sequence to download and install overlay, bitstream, and drivers from an AWS 
S3 bucket. The interface for this script is the same as the awsdownloader. 

Parameters
----------
s3bucket : str
    Name of the S3 bucket

s3directory : str
    Name of the S3 directory  in `s3bucket` where the desired files are located

driver_path : str
    Path prefix where the device drivers will be downloaded to; drivers are
    placed in a subdirectory of this path

config_path : str
    Where to put the UI.json and Linker.json config files

progress : list of str
    How to display download progress; options are 'bar' and 'json'

endpoint : str
    HTTP endpoint, specified as http://ip:port, to send download progress to

verbose : bool
    Print verbose output

Notes
-----
awsdownloader.py, overlaymgr, and drivermgr must be in the same directory as
this script. 

See Also
--------
awsdownloader.py

Copyright
---------
Copyright 2020 Flat Earth Inc

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Trevor Vannoy
Flat Earth Inc
985 Technology Blvd
Bozeman, MT 59718
support@flatearthinc.com
"""

import awsdownloader
import subprocess
import os
import sys


def main():
    # get the directory where this file is located.
    # we need this path so we can launch the overlaymgr and drivermgr scripts
    # when the script is called from somewhere else
    script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    # use the awsdownloader to parse command line arguments
    args = awsdownloader.parseargs()

    # download the files from AWS
    (firmware_files) = awsdownloader.main(args.bucket, args.directory, args.driver_path,
                       args.config_path, args.progress, args.endpoint, 
                       args.verbose)

    overlay_filename = next(file for file in firmware_files.names if ".dtbo" in file)
    overlay_name = overlay_filename.split(".")[0]

    # the drivermgr needs the project name, which can be
    # determined from the s3 directory: '<device_name>/<project_name>'
    project_name = args.directory.split('/')[-1].replace('-', '_')

    # load the overlay
    if args.verbose:
        subprocess.run([script_path + '/overlaymgr', '-v', '--dir', project_name, 'load', overlay_name])
    else:
        subprocess.run([script_path + '/overlaymgr', '--dir', project_name, 'load', overlay_name])
    

    # load the drivers
    if args.verbose:
        subprocess.run([script_path + '/drivermgr', '-v', 'load', project_name])
    else:
        subprocess.run([script_path + '/drivermgr', 'load', project_name])


if __name__ == "__main__":
    main()
