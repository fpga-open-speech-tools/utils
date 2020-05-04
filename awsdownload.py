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

firmware_path : str
    Path where the bitstream and device tree overlay will be downloaded to

driver_path : str
    Path prefix where the device drivers will be downloaded to; drivers are
    placed in a subdirectory of this path

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

Putting downloaded files in non-default path locations will affect the shell 
scripts that load the overlays and device drivers since they expect the files 
to be in the default locations. Using non-default locations is primarily for
debugging purposes. 

Examples
--------
Download files for the Audio Mini sound effects project
$ ./awsdownload.py -b nih-demos -d audiomini/sound-effects

Download files for the Audio Mini passthrough project, and put them in
non-default locations
$ ./awsdownload.py -b nih-demos -d audiomini/passthrough --firmware_path ~/firmware

Copyright
---------
Copyright 2020 Flat Earth Inc

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

DEFAULT_FIRMWARE_PATH = '/lib/firmware/'
DEFAULT_DRIVER_PATH = '/lib/modules/'


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
        '--firmware-path', type=str, default=DEFAULT_FIRMWARE_PATH,
        help="path where bitstreams and overlays get placed \
            (default: /lib/firmware/)")

    optional_args.add_argument(
        '--driver-path', type=str, default=DEFAULT_DRIVER_PATH,
        help="path prefix where kernel modules folder gets created \
            (default: /lib/modules/)")

    # Parse the arguments
    args = parser.parse_args()

    # Ensure firmware and driver paths end in a trailing slash
    if args.firmware_path[-1] != '/':
        args.firmware_path += '/'
    if args.driver_path[-1] != '/':
        args.driver_path += '/'

    return args


def main(s3bucket, s3directory, firmware_path=DEFAULT_FIRMWARE_PATH,
         driver_path=DEFAULT_DRIVER_PATH, verbose=False):
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

    firmware_path : str
        Path where the bitstream and device tree overlay will be downloaded to

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

    # Download the firmware files
    for key, filename in zip(firmware_keys, firmware_filenames):
        if verbose:
            print('Downloading file {} to {}...'.format(
                filename, firmware_path + filename))
        client.download_file(s3bucket, key, firmware_path + filename)

    # If the driver list isn't empty, download the drivers
    if driver_keys:
        for key, filename in zip(driver_keys, driver_filenames):
            if verbose:
                print('Downloading file {} to {}...'.format(
                    filename, driver_path + driver_group_name + '/' + filename))
            client.download_file(s3bucket, key, driver_path
                                 + driver_group_name + '/' + filename)


if __name__ == "__main__":
    args = parseargs()
    main(args.bucket, args.directory, args.firmware_path, args.driver_path,
         args.verbose)
