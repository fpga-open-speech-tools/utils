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

import boto3, sys, argparse
import os
from botocore.client import Config
from botocore import UNSIGNED

def parseargs():
    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Create a new group for the required arguments
    req_parser = parser.add_argument_group('Required Arguments')

    # Add arguments for the file name list, directory, and the bucket name
    # req_parser.add_argument('--file_list','-fl', nargs='+',help="List of filenames to download from the specified directory",type=str,required=True)
    req_parser.add_argument('--directory','-d',help="Directory to download files from",type=str,required=True)
    req_parser.add_argument('--bucket','-b',help="S3 bucket name",type=str,required=True)

    # Parse the arguments
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    args = parseargs()

    # Set the boto resource
    client = boto3.client('s3', region_name='us-west-2', config=Config(signature_version=UNSIGNED))

    objects = client.list_objects_v2(Bucket=args.bucket, Prefix=args.directory)['Contents']

    firmware_files = [obj['Key'] for obj in objects if '.rbf' in obj['Key'] or '.dtbo' in obj['Key']]
    driver_files = [obj['Key'] for obj in objects if '.ko' in obj['Key']]

    # TODO: driver files might be empty because the overlay may not need drivers, so we will need to handle this case...
    driver_dir = driver_files[0].split('/')[-2].replace('-','_')
    if not os.path.isdir('lib/modules/' + driver_dir):
        os.mkdir('lib/modules/' + driver_dir)

    for f in firmware_files:
        client.download_file(args.bucket, f, 'lib/firmware/' + f.split('/')[-1])
    for f in driver_files:
        client.download_file(args.bucket, f, 'lib/modules/' + driver_dir + '/' + f.split('/')[-1])

    print('All files downloaded')