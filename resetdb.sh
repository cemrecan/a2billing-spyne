#!/bin/sh -x

DBNAME=$(grep postgres:// a2billing-spyne.yaml | cut -d/ -f4);

if [ -z "$DBNAME" ]; then
    DBNAME=a2billing-spyne_$USER;
fi

dropdb -U postgres $DBNAME
createdb -U postgres $DBNAME || exit 1
a2bs_daemon --bootstrap --log-results
