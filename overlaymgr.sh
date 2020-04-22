#!/bin/bash
CONFIGFS_PATH=/sys/kernel/config/device-tree/overlays
FIRMWARE_PATH=/lib/firmware
VERBOSE=0

function load() {
    if [ $VERBOSE -eq 1 ]; then
        echo "Making device tree overlay directory"
        echo "    mkdir $CONFIGFS_PATH/$OVERLAY_NAME"
        echo
    fi;
    mkdir $CONFIGFS_PATH/$OVERLAY_NAME

    if [ $VERBOSE -eq 1 ]; then
        echo "Applying overlay"
        echo "    echo $OVERLAY_NAME.dtbo > $CONFIGFS_PATH/$OVERLAY_NAME/path"
        echo
    fi;
    (echo $OVERLAY_NAME.dtbo > $CONFIGFS_PATH/$OVERLAY_NAME/path)
}

function remove() {
    if [ $VERBOSE -eq 1 ]; then
        echo "Removing overlay directory"
        echo "    rmdir $CONFIGFS_PATH/$OVERLAY_NAME"
        echo
    fi;
    rmdir $CONFIGFS_PATH/$OVERLAY_NAME
}

function usage() {
    echo "Usage: overlaymgr load|remove overlay [-h|--help] [-v|--verbose]"
}

for arg in "$@"; do
    case $arg in
        -h | --help)
        usage
        exit
        ;;
        -v | --verbose)
        VERBOSE=1
        # pop argument off the argument array "$@"
        shift
        ;;
        --*)
        echo "Unrecognized argument: $arg" 1>&2
        usage
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

# make sure the user supplied two positional arguments
if [ ${#POSITIONAL_ARGS[*]} -ne 2 ]; then
    echo "Incorrect number of positional arguments." 1>&2
    usage
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
    usage
    exit 1
    ;;
esac
