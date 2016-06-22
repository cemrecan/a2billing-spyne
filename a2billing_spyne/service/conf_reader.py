#!usr/bin/env python
from a2billing_spyne.model import SipBuddies
from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

with closing(open("sip.conf")) as file:
    table = file.readlines()

sip = SipBuddies._type_info

db = create_engine('postgres://postgres:@localhost:5432/radius')

session = Session(db)

name = None
qualify = None
type = None
host = None
context = None
secret = None
dtmfmode = None
callerid = None

for line in table:
    if line[0] == '[':
        if name is not None and name != 'general':
            session.add(SipBuddies(
                name=name,
                qualify=qualify,
                type=type,
                host=host,
                context=context,
                secret=secret,
                dtmfmode=dtmfmode,
                callerid=callerid,
            ))
            session.flush()
        name = line.split()
        name = (name[0])[1:-1]
    else:
        data = line.split("=")
        if name is not None and name != 'general' and data[0].isalpha():
            if data[0] in sip.keys():
                if data[0] == "qualify" and len(data) >= 2:
                    qualify = data[1]
                elif data[0] == "type" and len(data) >= 2:
                    type = data[1]
                elif data[0] == "host" and len(data) >= 2:
                    host = data[1]
                elif data[0] == "context" and len(data) >= 2:
                    context = data[1]
                elif data[0] == "secret" and len(data) >= 2:
                    secret = data[1]
                elif data[0] == "dtmfmode" and len(data) >= 2:
                    dtmfmode = data[1]
                elif data[0] == "callerid" and len(data) >= 2:
                    callerid = data[1]
            print name,data

session.commit()