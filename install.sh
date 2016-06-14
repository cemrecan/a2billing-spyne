#!/bin/bash -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd

if [ ! -x `which virtualenv` ]; then
    echo virtualenv not found
    exit 1;
fi;

if [ ! -d virt-2.7 ]; then
    rm -rf virt-2.7;
    virtualenv virt-2.7;
fi

source virt-2.7/bin/activate;

pip install --upgrade pip
pip install --upgrade "$DIR"/wheels/spyne-*;
pip install --upgrade "$DIR"/wheels/neurons-*;
pip install --upgrade "$DIR"/wheels/a2billing_spyne-*;

if [ -d "$DIR"/assets ]; then 

    (
        cd "$DIR";

        chmod go-rwx assets
        find assets -type d -print0 | xargs -0 chmod go+x;
        find assets -type f -print0 | xargs -0 chmod go+r;
    );

    rm -rf assets
    mv -v "$DIR"/assets .

fi
