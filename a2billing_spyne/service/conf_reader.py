#!usr/bin/env python
from a2billing_spyne.model import SipBuddy, Extensions
from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

with closing(open("sip.conf")) as file:
    table = file.readlines()

sip = SipBuddy._type_info

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
            session.add(SipBuddy(
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
                    qualify = (data[1])[:-1]
                elif data[0] == "type" and len(data) >= 2:
                    type = (data[1])[:-1]
                elif data[0] == "host" and len(data) >= 2:
                    host = (data[1])[:-1]
                elif data[0] == "context" and len(data) >= 2:
                    context = (data[1])[:-1]
                elif data[0] == "secret" and len(data) >= 2:
                    secret = (data[1])[:-1]
                elif data[0] == "dtmfmode" and len(data) >= 2:
                    dtmfmode = (data[1])[:-1]
                elif data[0] == "callerid" and len(data) >= 2:
                    callerid = (data[1])[:-1]

session.commit()


with closing(open("extensions.conf")) as file:
    table = file.readlines()

exten = None
priority = None
app = None
appdata = None
context = None

sip_buddies = session.query(SipBuddy).all()
contexts = set()

for sb in sip_buddies:
    contexts.add(sb.context)

for line in table:
    if line[0] == '[':
        context = line.split()
        context = (context[0])[1:-1]
        print context

    else:
        data = line.split(" => ")
        if context is not None and context in contexts and data[0].isalpha():
            appdatavalue = data[1].split("(")
            areas = appdatavalue[0].split(",")

            exten = areas[0]

            priority = areas[1]

            app = areas[2]

            appdata = (appdatavalue[1])[:-2]

            print data[0], exten, priority, app, appdata

    if context in contexts:
        session.add(Extensions(
            exten=exten,
            priority=priority,
            app=app,
            appdata=appdata,
            context=context,
        ))
        session.flush()


session.commit()

