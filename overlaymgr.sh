#!/bin/bash

# overlaymgr.sh
#
# Load and remove device tree overlays.
#
# Usage: overlaymgr.sh load <overlay_name>
#        overlaymgr.sh remove <overlay_name>
# 
# This script uses the configfs overlay interface to load and 
# remove device tree overlays at runtime. The overlays can
# program the FPGA via the fpga manager, as well as add/remove
# nodes in the device tree. In general, our overlays will do
# both of the preceeding, but that need not always be the case.
#
# The overlay (.dtbo) and the FPGA bitstream (.rbf) need to be
# located in /lib/firmware before running this script. It is assumed
# that the overlay and bitstream have the same name, and are named according
# to the Quartus project they came from.  
#
# See documentation/devicetree/configfs-overlays.txt in the kernel documentation
# for more information on the configfs overlay interface.
#
# author Trevor Vannoy
# copyright 2020 Flat Earth Inc
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Trevor Vannoy
# Flat Earth Inc
# 985 Technology Blvd
# Bozeman, MT 59718
# support@flatearthinc.com

CONFIGFS_PATH=/sys/kernel/config/device-tree/overlays
VERBOSE=0
POSITIONAL_ARGS=()

# Load the device tree overlay
#
# To load an overlay, we first need to create a directory in the configfs 
# pseudofilesystem: /sys/kernel/config/device-tree/overlays/<overlay_name>
# The kernel mounts configfs at /sys/kernel/config, and creates the 
# device-tree/overlays directory for us. We echo the overlay file name to the
# path property file that gets created for us in the <overlay_name> directory.
function load() {
    if [ $VERBOSE -eq 1 ]; then
        echo "Making device tree overlay directory"
        echo "    mkdir $CONFIGFS_PATH/$OVERLAY_NAME"
        echo
    fi
    # make the overlay directory in configfs
    mkdir $CONFIGFS_PATH/$OVERLAY_NAME

    if [ $VERBOSE -eq 1 ]; then
        echo "Applying overlay"
        echo "    echo $OVERLAY_NAME.dtbo > $CONFIGFS_PATH/$OVERLAY_NAME/path"
        echo
    fi
    # echo the overlay file name to the path property file
    (echo $OVERLAY_NAME.dtbo > $CONFIGFS_PATH/$OVERLAY_NAME/path)
}

# Remove the device tree overlay.
#
# Overlays are removed by removing the configfs overlay directory we created:
# /sys/kernel/config/device-tree/overlays/<overlay_name>. This removes nodes
# from the device tree, but it doesn't unload the FPGA bitstream. When used to 
# program the FPGA, overlays must be removed before loading in a new overlay 
# (according to empirical testing, anyway). 
function remove() {
    if [ $VERBOSE -eq 1 ]; then
        echo "Removing overlay directory"
        echo "    rmdir $CONFIGFS_PATH/$OVERLAY_NAME"
        echo
    fi
    # remove the configfs overlay directory
    rmdir $CONFIGFS_PATH/$OVERLAY_NAME
}

# Print verbose usage help
function usage() {
    short_usage
    echo
    echo "Load and remove device tree overlays."
    echo 
    echo "commands:"
    echo "  load            load a device tree overlay"
    echo "  remove          remove a device tree overlay"
    echo
    echo "positional arguments:"
    echo "  OVERLAY         the name of the overlay file to load/remove"
    echo 
    echo "optional arguments:"
    echo "  -h, --help      display this help text"
    echo "  -v, --verbose   print more details about what's going on"
}

# Print brief usage help
#
# Primarily for when user's invoke the script incorrectly.
function short_usage() {
    echo "usage: overlaymgr [-h] [-v] <COMMAND> OVERLAY"
}


# argument parsing
while [[ "$#" -gt 0 ]]; do
    arg="$1"
    case $arg in
        -h|--help)
        usage
        exit
        ;;
        -v|--verbose)
        VERBOSE=1
        # pop argument off the argument array "$@"
        shift
        ;;
        --*)
        echo "Unrecognized argument: $arg" 1>&2
        echo
        short_usage
        exit 1
        ;;
        *)
        # add positional argument to positional arguments array for later
        POSITIONAL_ARGS+=("$1")
        # pop argument off the argument array "$@"
        shift
        ;;
    esac
done

if [ ${#POSITIONAL_ARGS[*]} -eq 0 ]; then
    # print help when no arguments are supplied
    usage
    exit 1
elif [ ${#POSITIONAL_ARGS[*]} -ne 2 ]; then
    # make sure the user supplied two positional arguments
    echo "Incorrect number of positional arguments." 1>&2
    echo
    short_usage
    exit 1
fi

# grab command and overlay name from the positional arguments
COMMAND=${POSITIONAL_ARGS[0]}
OVERLAY_NAME=${POSITIONAL_ARGS[1]}

# run the command
case $COMMAND in
    load)
    load
    ;;
    remove)
    remove
    ;;
    *)
    echo "Incorrect command. Must be either \"load\" or \"remove\"." 1>&2
    echo
    short_usage
    exit 1
    ;;
esac
