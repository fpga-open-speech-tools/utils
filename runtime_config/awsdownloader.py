#!/usr/bin/python3
"""
Download files for an SoC FPGA project from AWS.

This script downloads the bitstream, device tree overlay, and device
drivers located in a user-supplied directory in a user-supplied S3 bucket.

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

verbose : bool
    Print verbose output

Notes
-----
boto3 and tqdm must be installed on the system in order to run this script; 
they can both be installed with pip.

By convention, S3 directories are all lowercase, with words separated by hyphens
when doing so improves readability. For example, the directory for the 
Audio Mini sound effects project is audiomini/sound-effects. Additionally,
The bitstream and device tree overlays are named the same as the project, but
with underscores instead of hyphens, e.g. sound_effects.rbf. 

The directory name can be given with or without a trailing slash.

The .dtbo and .rbf files need to be on the firmware search path, so they 
will always be placed in /lib/firmware. If placing drivers in a non-default
path, users will need to supply that path as an argument to drivermgr.sh. 

Displaying download progress as json messages is intended to be read by 
another program that can display a progress bar to a user on a web app.

In order for the progress monitor bar to work to stay at the bottom of the
console output, tqdm.write() is used instead of print().

Examples
--------
Download files for the Audio Mini sound effects project
$ ./awsdownloader.py -b nih-demos -d audiomini/sound-effects

Download files for the Audio Mini passthrough project and show a progress bar
# ./awsdownloader.py -b nih-demos -d audiomini/passthrough --progress bar

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
import json
from tqdm import tqdm
from collections import namedtuple
from botocore.client import Config
from botocore import UNSIGNED

FIRMWARE_PATH = '/lib/firmware/'
DEFAULT_DRIVER_PATH = '/lib/modules/'
DEFAULT_CONFIG_PATH = '../config/'
FIRMWARE_EXTENSIONS = ('.rbf', '.dtbo')
DRIVER_EXTENSIONS = ('.ko')
CONFIG_EXTENSIONS = ('.json')

"""
Named tuple to group together info about S3 files.

Parameters
----------
names
    A tuple or list of file names
keys
    A tuple or list of the S3 keys corresponding to the files
sizes
    A tuple or list of the file sizes in bytes
"""
_S3Files = namedtuple('S3Files', ['names', 'keys', 'sizes'])


class _ProgressMonitor(object):
    """
    A download progress monitor.

    Monitors the download progress of all the S3 files and displays a
    progress indicator on stdout. This class is used as the callback
    to the boto3 download_files method, which calls the __call__ method.

    Parameters
    ----------
    total_download_size
        Size of all the S3 files being downloaded, in bytes
    show_json : bool
        Show download progress as a json message
    show_bar : bool
        Show download progress as a progress bar

    Attributes
    ----------
    status : str
        User-definable download status message
    bytes_received : int
        The number of bytes received from S3 so far
    percent_downloaded : int
        How much of the files have been downloaded so far
    json_status_message : dict
        Download status message and progress as JSON

    Notes
    -----
    The JSON status message can be read from stdout and used by other programs
    to report the download progress/status. It's format is
    {"progress": 42, "status": "downloading file x"}
    """

    def __init__(self, total_download_size, show_json=False, show_bar=False):
        self.total_download_size = total_download_size
        self.show_json = show_json
        self.show_bar = show_bar
        self.status = ""
        self.bytes_received = 0
        self.percent_downloaded = 0
        self.json_status_message = {
            "progress": 0,
            "status": ""
        }

        if self.show_bar:
            self._progress_bar = tqdm(
                bar_format='{l_bar}{bar}| {n_fmt}B/{total_fmt}B [{elapsed}]', desc="Downloading", total=self.total_download_size,
                mininterval=0.05, unit_scale=True)
        else:
            self._progress_bar = None

    def __call__(self, bytes_received):
        """
        Update and print the download progress.

        Download progress is only printed is show_json and/or show_bar are True.

        Parameters
        ----------
        bytes_received : int
            The number of bytes received since the previous callback from boto3
        """
        self.bytes_received += bytes_received
        self.percent_downloaded = (
            int(self.bytes_received / self.total_download_size * 100)
        )
        self.json_status_message['progress'] = self.percent_downloaded
        self.json_status_message['status'] = self.status

        if self.show_json:
            tqdm.write(json.dumps(self.json_status_message))
        if self.show_bar:
            self._progress_bar.update(bytes_received)


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
        '--config-path', type=str, default=DEFAULT_CONFIG_PATH,
        help="where to put the UI.json and Linker.json config files \
            (default: " + DEFAULT_CONFIG_PATH + ")"
    )
    optional_args.add_argument(
        '-p', '--progress', action='append', choices=['bar', 'json'],
        default=[], help="progress monitoring; 'bar' displays a progress bar, \
            and 'json' displays progress in json format; multiple arguments \
            can be given",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Ensure paths ends in a trailing slash
    if args.driver_path[-1] != '/':
        args.driver_path += '/'
    if args.config_path[-1] != '/':
        args.config_path += '/'

    return args


def _get_file_info(s3objects, file_extensions):
    """
    Get information about files in an s3 objects list.

    Given a list of s3 objects, this function extracts the key, filename, 
    and file size for each file that ends in an extension in `file_extensions`

    Parameters
    ----------
    s3objects : list
        List of dictionaries return by boto3's download_file()

    file_extensions : tuple
        File extensions to match keys against

    Returns
    -------
    _S3Files
        A named tuple containing tuples of file names, keys, and sizes

    Notes
    -----
    boto3's list_objects_v2 returns a dictionary of information about the S3
    objects. Within the 'Contents' key, which is what needs to be fed to this
    function, each object in the list has 'Key' and 'Size' keys. 
    The 'Key' attribute is of the form "some/directory/filename.extension". 
    """
    # Get firmware keys that end with any extension in file_extensions
    keys = tuple(obj['Key'] for obj in s3objects
                 if obj['Key'].endswith(file_extensions))

    # If no keys matching file_extensions were found, exit early
    if not keys:
        return None

    # Get firmware filenames (the part of the key after the last slash)
    # A typical key will be '<device name>/<project name>/<file name>'
    names = tuple(key.split('/')[-1] for key in keys)

    # Get file sizes for all keys that end with an extension in file_extensions
    sizes = tuple(obj['Size'] for obj in s3objects
                  if obj['Key'].endswith(file_extensions))

    # Pack everything into a _S3Files named tuple
    return _S3Files(names=names, keys=keys, sizes=sizes)


def main(s3bucket, s3directory, driver_path=DEFAULT_DRIVER_PATH,
         config_path=DEFAULT_CONFIG_PATH, progress=[], verbose=False):
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

    config_path : str
        Where to put the UI.json and Linker.json config files

    progress : list of str
        How to display download progress; valid options are 'bar' and 'json'

    verbose : bool
        Print verbose output
    """
    project_name = s3directory.split('/')[-1].replace('-', '_')

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

    # Get info about the firmware files in the s3 directory
    firmware_files = _get_file_info(objects, FIRMWARE_EXTENSIONS)

    # Kill the program if the s3 directory doesn't have firmware files
    if firmware_files is None:
        print("The s3 directory {} does not contain an overlay".format(
            s3directory), file=sys.stderr)
        exit(1)

    total_download_size = sum(firmware_files.sizes)

    # Get info about any driver files in the s3 directory
    driver_files = _get_file_info(objects, DRIVER_EXTENSIONS)

    if driver_files:
        # Create a directory for the drivers if one doesn't already exist
        if not os.path.isdir(driver_path + project_name):
            os.mkdir(driver_path + project_name)

        total_download_size += sum(driver_files.sizes)

    # Get info about any config files in the s3 directory
    config_files = _get_file_info(objects, CONFIG_EXTENSIONS)

    if config_files:
        # Create a directory for the config files if one doesn't already exist
        if not os.path.isdir(config_path):
            os.mkdir(config_path)

        total_download_size += sum(config_files.sizes)

    # Set up a progress monitor
    show_bar = False
    show_json = False
    if 'bar' in progress:
        show_bar = True
    if 'json' in progress:
        show_json = True
    progressMonitor = _ProgressMonitor(
        total_download_size, show_bar=show_bar, show_json=show_json)

    # Download the firmware files
    for (key, filename) in zip(firmware_files.keys, firmware_files.names):
        progressMonitor.status = "downloading {}".format(key)

        if verbose:
            tqdm.write('Downloading file {} to {}...'.format(
                filename, FIRMWARE_PATH + filename))

        client.download_file(s3bucket, key, FIRMWARE_PATH + filename,
                             Callback=progressMonitor)

    # If there are driver files, download them
    if driver_files:
        for key, filename in zip(driver_files.keys, driver_files.names):
            progressMonitor.status = "downloading {}".format(key)

            if verbose:
                tqdm.write('Downloading file {} to {}...'.format(
                    filename, driver_path + project_name + '/' + filename))

            client.download_file(s3bucket, key, driver_path + project_name
                                 + '/' + filename, Callback=progressMonitor)

    # If there are config files, download them
    if config_files:
        for key, filename in zip(config_files.keys, config_files.names):
            progressMonitor.status = "downloading {}".format(key)

            if verbose:
                tqdm.write('Downloading file {} to {}...'.format(
                    filename, config_path + filename))

            client.download_file(s3bucket, key, config_path + filename,
                                 Callback=progressMonitor)


if __name__ == "__main__":
    args = parseargs()
    main(args.bucket, args.directory, args.driver_path,
         args.config_path, args.progress, args.verbose)
