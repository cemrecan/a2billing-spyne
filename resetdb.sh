#!/bin/sh -x

dropdb -U postgres a2billing-spyne_$USER
createdb -U postgres a2billing-spyne_$USER || exit 1
a2bs_daemon --bootstrap --log-results