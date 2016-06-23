#!usr/bin/env python

from a2billing_spyne.model import SipBuddy
from contextlib import closing

class File():
    with closing(open("siptry.conf")) as file:
        table = file.readlines()

    sip = SipBuddy._type_info

    for line in table:
        if line[0] == '[':
            name = line.split()
            print name[0]
        else:
            data = line.split("=")
            print data[0]
            if len(data) >= 2:
                print data[1]
""""
class ToDatabase():
    def put_sip(self,sipbuddy):
    ????with closing(self.ctx.app.config.get_main_store().Session()) as session:
            session.add(sipbuddy)
            session.commit()
            return sipbuddy
"""
