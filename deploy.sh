#!/bin/bash

# you need to login via pubkey to the remote server to 
# keep your sanity while using this script

##############
# INIT

unset PYTHONDONTWRITEBYTECODE
REMOTE_HOST="$1";
REMOTE_USER="$2";
REMOTE_PORT='22';
PYTHON=python2;
# http://stackoverflow.com/a/246128/1520211
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

[ -z "$DIR" ] && exit 2;

##############
# LIB

pap() {
    echo $(dirname "$(python -c "import $1; print $1.__file__")"); #"
}

prp() {
    retval="$1";
    retval="$(pap "$retval")";
    retval=$(readlink -f "$retval");

    while [ ! -e "$retval"/setup.py ]; do
        retval="$( dirname "$retval" )";
        if [ "$retval" == "." ]; then
            echo $1 icin setup.py bulunamadi;
            exit 2;
        fi
    done;
    echo "$retval"
}

get_wheel() {
    package=$1;
    proj_path="$(prp "$package")";

    [ -z "$proj_path" ] && exit 2;
    rm -rf $proj_path/build $proj_path/dist

    (cd "$proj_path"; $PYTHON setup.py bdist_wheel || exit 1) || exit 1
    mv "$proj_path"/dist/*.whl wheels;
}

usage() {
    echo Usage: $0 "<host>" "[user]";
    exit 1;
}

##############
# MAIN

if [ ! -n "$1" ]; then
   usage;
fi

if [ ! -n "$REMOTE_USER" ]; then
   REMOTE_USER="a2bs";
fi

cd "$DIR"; rm -rf wheels; mkdir -p wheels;

get_wheel spyne
get_wheel neurons
get_wheel a2billing_spyne

REMOTE="$REMOTE_USER@$REMOTE_HOST"

ssh "$REMOTE" -p $REMOTE_PORT "mkdir -p deploy";

rsync --fuzzy -azPe "ssh -p $REMOTE_PORT" --delete-excluded --delete \
    wheels install.sh resetdb.sh ${REMOTE}:deploy || exit 1

ssh "$REMOTE" -p $REMOTE_PORT "deploy/install.sh";
