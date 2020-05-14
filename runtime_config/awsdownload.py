#!/usr/bin/python3
"""
Download files for an SoC FPGA project from AWS.

This script downloads the bitstream, device tree overlay, and device
drivers located in a user-supplied directory in a user-supplied S3 bucket.

Parameters
---------
s3bucket : str
    Name of the S3 bucket

s3directory : str
    Name of the S3 directory  in `s3bucket` where the desired files are located

driver_path : str
    Path prefix where the device drivers will be downloaded to; drivers are
    placed in a subdirectory of this path

json_path : str
    Where to put the UI.json and Linker.json files

verbose : bool
    Print verbose output

Notes
-----
boto3 must be installed on the system in order to run this script.

By convention, S3 directories are all lowercase, with words separated by hyphens
when doing so improves readability. For example, the directory for the 
Audio Mini sound effects project is audiomini/sound-effects. Additionally,
The bitstream and device tree overlays are named the same as the project, but
with underscores instead of hyphens, e.g. sound_effects.rbf. 

The directory name can be given with or without a trailing slash.

The .dtbo and .rbf files need to be on the firmware search path, so they 
will always be placed in /lib/firmware. If placing drivers in non-default path,
users will need to supply that path as an argument to drivermgr.sh. 

Example
-------
Download files for the Audio Mini sound effects project
$ ./awsdownload.py -b nih-demos -d audiomini/sound-effects

Copyright
---------
Copyright 2020 Audio Logic

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Trevor Vannoy, Tyler Davis
Audio Logic
985 Technology Blvd
Bozeman, MT 59718
openspeech@flatearthinc.com
"""

import boto3
import sys
import argparse
import os
from botocore.client import Config
from botocore import UNSIGNED

FIRMWARE_PATH = '/lib/firmware/'
DEFAULT_DRIVER_PATH = '/lib/modules/'
DEFAULT_JSON_PATH = '../config/'


def parseargs():
    """
    Parse command-line arguments.

    Returns
    -------
    args : Namespace
        Object containing the parsed arguments
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(add_help=False)

    # Create a new group for the required arguments
    required_args = parser.add_argument_group('required arguments')

    # Add arguments for the directory and the bucket name
    required_args.add_argument('-d', '--directory', type=str, required=True,
                               help="S3 directory to download files from")
    required_args.add_argument('-b', '--bucket', type=str, required=True,
                               help="S3 bucket name")

    # Create a group for optional arguments so required arguments print first
    optional_args = parser.add_argument_group('optional arguments')

    # Add optional arguments
    optional_args.add_argument('-h', '--help', action='help',
                               help="show this help message and exit")
    optional_args.add_argument('-v', '--verbose', action='store_true',
                               help="print verbose output", default=False)
    optional_args.add_argument(
        '--driver-path', type=str, default=DEFAULT_DRIVER_PATH,
        help="path prefix where kernel modules folder gets created \
            (default: " + DEFAULT_DRIVER_PATH + ")"
    )
    optional_args.add_argument(
        '--json-path', type=str, default=DEFAULT_JSON_PATH,
        help="where to put the UI.json and Linker.json config files \
            (default: " + DEFAULT_JSON_PATH + ")"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Ensure paths ends in a trailing slash
    if args.driver_path[-1] != '/':
        args.driver_path += '/'
    if args.json_path[-1] != '/':
        args.json_path += '/'

    return args


def main(s3bucket, s3directory, driver_path=DEFAULT_DRIVER_PATH,
         json_path=DEFAULT_JSON_PATH, verbose=False):
    """
    Download files for an SoC FPGA project from AWS. 

    This script downloads the bitstream, device tree overlay, and device
    drivers located in a user-supplied directory in a user-supplied S3 bucket.

    Parameters
    ----------
    s3bucket : str
        Name of the S3 bucket

    s3directory : str
        Name of the S3 directory  in `s3bucket` where the desired files are

    driver_path : str
        Path prefix where the device drivers will be downloaded to; drivers are
        placed in a subdirectory of this path

    verbose : bool
        Print verbose output
    """
    # Create an s3 client that doesn't need/use aws credentials
    client = boto3.client('s3', region_name='us-west-2',
                          config=Config(signature_version=UNSIGNED))

    # Get all of the s3 objects that are in the desired bucket and directory.
    # The "directory" isn't really a directory, but a prefix in the object keys,
    # e.g. Key: some/directory/<actual_file>
    # list_objects_v2 returns a big dictionary about the objects; the Contents
    # key is what contains the actual directory contents
    objects = client.list_objects_v2(
        Bucket=s3bucket, Prefix=s3directory)['Contents']

    # Get the keys for the bitstream (.rbf) and device tree overlay (.dtbo)
    firmware_keys = [obj['Key'] for obj in objects
                     if '.rbf' in obj['Key'] or '.dtbo' in obj['Key']]

    # Get the keys for the device drivers (.ko files)
    # If no drivers are in the s3 "directory", this list will be empty
    driver_keys = [obj['Key'] for obj in objects if '.ko' in obj['Key']]

    # Get the keys for the UI.json and Linker.json config files
    # It's possible that a project will not have json config files
    json_keys = [obj['Key'] for obj in objects if '.json' in obj['Key']]

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

    # If there are json config files
    if json_keys:
        # Create a config directory if it doesn't already exist
        if not os.path.isdir(json_path):
            os.mkdir(json_path)

        # Get the json filenames
        json_filenames = [key.split('/')[-1] for key in json_keys]

    # Download the firmware files
    for key, filename in zip(firmware_keys, firmware_filenames):
        if verbose:
            print('Downloading file {} to {}...'.format(
                filename, FIRMWARE_PATH + filename))
        client.download_file(s3bucket, key, FIRMWARE_PATH + filename)

    # If the driver list isn't empty, download the drivers
    if driver_keys:
        for key, filename in zip(driver_keys, driver_filenames):
            if verbose:
                print('Downloading file {} to {}...'.format(
                    filename, driver_path + driver_group_name + '/' + filename))
            client.download_file(s3bucket, key, driver_path
                                 + driver_group_name + '/' + filename)

    # If there json config files, download them
    if json_keys:
        for key, filename in zip(json_keys, json_filenames):
            if verbose:
                print('Downloading file {} to {}...'.format(
                    filename, json_path + '/' + filename))
            client.download_file(s3bucket, key, json_path + '/' + filename)


if __name__ == "__main__":
    args = parseargs()
    main(args.bucket, args.directory, args.driver_path,
         args.json_path, args.verbose)
