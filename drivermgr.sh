#!/bin/bash
BASE_MODULES_PATH=/lib/modules
VERBOSE=0

function load() {
    for module in $MODULES_PATH/*.ko; do
        if [ $VERBOSE -eq 1 ]; then
            echo "loading kernel module: $module"
        fi
        insmod $module
    done
}

function remove() {
    for module in $MODULES_PATH/*.ko; do
        if [ $VERBOSE -eq 1 ]; then
            echo "removing kernel module: $module"
        fi
        rmmod $module
    done
}

function usage() {
    echo "Usage: drivermgr load|remove directory [-h|--help] [-v|--verbose]"
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

# make sure the user supplied 2 arguments
if [ ${#POSITIONAL_ARGS[*]} -ne 2 ]; then
    echo "Incorrect number of positional arguments." 1>&2
    usage
    exit 1
fi

# grab command and overlay name from the positional arguments
COMMAND=${POSITIONAL_ARGS[0]}
MODULES_PATH=$BASE_MODULES_PATH/${POSITIONAL_ARGS[1]}

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
