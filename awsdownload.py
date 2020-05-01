#!/usr/bin/python3
"""
This is a basic script that will download the specified files from an S3 bucket

Arguments
---------
file_list : str, list
    List of files to download from the S3 bucket

directory : str
    Directory in which all the files are located

bucket    : str
    Name of the S3 bucket to download files from

Example
-------
In this example, the user only wants to download a single file called DE10Nano_System.sof.  This is accomplished by 
calling the script and providing three keyword arguments; the list of files (--file_list or -f), the directory of the 
files (--directory or -d) and the name of  the S3 bucket (--bucket or -b).  The file is located in the nih-demos bucket 
in the directory DE10-Nano/Passthrough/, so the function call  is as follows:

python3 download_files.py -fl DE10Nano_System.sof -b nih-demos -d DE10-Nano/Passthrough/ 

Upon successful completion, the script will return :

All files downloaded

If more than one file in the directory needs to be downloaded, simply add more filenames to the list.  
(e.g. -fl DE10Nano_system.sof soc_system.dtb DE10Nano_system.rbf)

Notes
-----
In order to run this script, the Amazon CLI credentials must be setup on the system.  This can be done by installing 
AWS CLI using 

sudo apt-get install awscli

then following the configuration instructions after executing 

aws configure

boto3 must also be installed on the system in order to run this script.  This is accomplished by executing 

pip3 install boto3


Copyright 2020 Flat Earth Inc

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Trevor Vannoy, Tyler Davis
Flat Earth Inc
985 Technology Blvd
Bozeman, MT 59718
support@flatearthinc.com

"""

import boto3
import sys
import argparse
import os
from botocore.client import Config
from botocore import UNSIGNED
from time import time

def parseargs():
    # Create the argument parser
    parser = argparse.ArgumentParser(add_help=False)

    # Create a new group for the required arguments
    required_args = parser.add_argument_group('required arguments')

    # Add arguments for the directory and the bucket name
    required_args.add_argument('-d', '--directory', help="S3 directory to download files from", type=str, required=True)
    required_args.add_argument('-b', '--bucket', help="S3 bucket name", type=str, required=True)

    # Create an explicit group for optional arguments so the required arguments print first
    optional_args = parser.add_argument_group('optional arguments')

    # Add optional arguments
    optional_args.add_argument('-h', '--help', help="show this help message and exit", action='help')
    optional_args.add_argument('-v', '--verbose', help="print verbose output", default=False, action='store_true')
    optional_args.add_argument('--firmware-path', help="path where bitstreams and overlays get placed (default: /lib/firmware/)", type=str, default='/lib/firmware/')
    optional_args.add_argument('--driver-path', help="path prefix where kernel modules folder gets created (default: /lib/modules/)", type=str, default='/lib/modules/')

    # Parse the arguments
    args = parser.parse_args()

    # Ensure firmware and driver paths end in a trailing slash
    if args.firmware_path[-1] != '/':
        args.firmware_path += '/'
    if args.driver_path[-1] != '/':
        args.driver_path += '/'

    return args


def main(s3bucket, s3directory, firmware_path, driver_path, verbose):
    # Create an s3 client that doesn't need/use aws credentials
    client = boto3.client('s3', region_name='us-west-2', config=Config(signature_version=UNSIGNED))

    # Get all of the s3 objects that are in the desired bucket and directory.
    # The "directory" isn't really a directory, but a prefix in the object keys,
    # e.g. Key: some/directory/<actual_file>
    objects = client.list_objects_v2(Bucket=s3bucket, Prefix=s3directory)['Contents']

    # Get the keys for the bitstream (.rbf) and device tree overlay (.dtbo)
    firmware_keys = [obj['Key'] for obj in objects if '.rbf' in obj['Key'] or '.dtbo' in obj['Key']]

    # Get the keys for the device drivers (.ko files)
    # If no drivers are in the s3 "directory", this list will be empty
    driver_keys = [obj['Key'] for obj in objects if '.ko' in obj['Key']]

    # Get the firmware filenames (the part of the key after the last slash)
    firmware_filenames = [key.split('/')[-1] for key in firmware_keys]

    # If the driver list isn't empty
    if driver_keys:
        # Get the project name that these drivers belong to. By convention, 
        # this should be the same as the firmware file names (without the 
        # file extension). 
        driver_group_name = firmware_filenames[0].split('.')[0]

        # Create a directory for the drivers if one doesn't already exist
        if not os.path.isdir(driver_path + driver_group_name):
            os.mkdir(driver_path + driver_group_name)

        # Get the driver filenames
        driver_filenames = [key.split('/')[-1] for key in driver_keys]

    start = time()
    # Download the firmware files
    for key,filename in zip(firmware_keys, firmware_filenames):
        client.download_file(s3bucket, key, firmware_path + filename)
    
    # If the driver list isn't empty, download the drivers
    if driver_keys:
        for key,filename in zip(driver_keys, driver_filenames):
            client.download_file(s3bucket, key, driver_path + 
                driver_group_name + '/' + filename)
    end = time()
    print(end - start)

    print('All files downloaded')




if __name__ == "__main__":
    args = parseargs()
    main(args.bucket, args.directory, args.firmware_path, args.driver_path,
        args.verbose)
