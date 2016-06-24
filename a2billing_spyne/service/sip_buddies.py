# encoding: utf8
#
# This file is part of the a2billing-spyne project.
# Copyright (c), Arskom Ltd. (arskom.com.tr),
#                Cemrecan Ünal <unalcmre@gmail.com>.
#                Burak Arslan <burak.arslan@arskom.com.tr>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the Arskom Ltd. nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#



from contextlib import closing

from lxml.html.builder import E

from twisted.internet.threads import deferToThread

from spyne import rpc, Array
from spyne.const.http import HTTP_302
from spyne.protocol.html.table import HtmlColumnTable

from neurons.form import HtmlForm, HrefWidget

from a2billing_spyne.model import SipBuddy
from a2billing_spyne.service import ReaderServiceBase, ScreenBase, DalBase


SIP_BUDDY_CUST = dict(
    name=dict(order=1, exc=False),
    callerid=dict(order=2, exc=False),
    context=dict(order=3, write=False, exc=False),
    dtmfmode=dict(order=4, exc=False),
    host=dict(order=5, write=False, exc=False),
    secret=dict(order=6, exc=False),
    type=dict(order=7, exc=False),
)


SipBuddyScreen = SipBuddy.customize(
    prot=HtmlForm(), form_action="put_sip_buddy",
    child_attrs_all=dict(exc=True,),
    child_attrs=dict(
        id=dict(order=0, write=False, exc=False),
        **SIP_BUDDY_CUST
    ),
)


class NewSipBuddyScreen(ScreenBase):
    main = SipBuddyScreen


class SipBuddyDetailScreen(ScreenBase):
    main = SipBuddyScreen


def _write_new_sip_buddy_link(ctx, cls, inst, parent, name, *kwargs):
    parent.write(E.a("New SipBuddy", href="/new_sip_buddy"))


class SipBuddyListScreen(ScreenBase):
    main = Array(
        SipBuddy.customize(
            child_attrs_all=dict(exc=True,),
            child_attrs=dict(
                id=dict(prot=HrefWidget("/get_sip_buddy?id={}")),
            **SIP_BUDDY_CUST
            ),
        ),
        prot=HtmlColumnTable(before_table=_write_new_sip_buddy_link),
    )


class SipBuddyDal(DalBase):
    def put_sip_buddy(self, sip_buddy):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            sip_buddy.qualify = 'yes'
            session.add(sip_buddy)
            session.commit()
            return sip_buddy

    def get_sip_buddy(self, sip_buddy):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            return session.query(SipBuddy).filter(SipBuddy.id ==
                                                            sip_buddy.id).one()
    def get_all_sip_buddy(self, sip_buddy):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            return session.query(SipBuddy).all()

class SipBuddyReaderServices(ReaderServiceBase):
    @rpc(SipBuddy.novalidate_freq(), _returns=NewSipBuddyScreen,
         _body_style='bare')
    def new_sip_buddy(ctx, sip_buddy):
        return NewSipBuddyScreen(title="New Sip Buddy", main=sip_buddy)

    @rpc(SipBuddy.novalidate_freq(), _returns=SipBuddyDetailScreen,
         _body_style='bare')
    def get_sip_buddy(ctx,sip_buddy):
        return deferToThread(SipBuddyDal(ctx).get_sip_buddy, sip_buddy) \
            .addCallback(lambda ret:
                         SipBuddyDetailScreen(title="Get Sip Buddy", main=ret))

    @rpc(SipBuddy.novalidate_freq(), _returns=SipBuddyListScreen, _body_style='bare')
    def get_all_sip_buddy(ctx, sip_buddy):
        return deferToThread(SipBuddyDal(ctx).get_all_sip_buddy, sip_buddy) \
            .addCallback(lambda ret: SipBuddyListScreen(title="Sip Buddies",
                                                                      main=ret))


class SipBuddyWriterServices(ReaderServiceBase):
    @rpc(SipBuddy, _body_style='bare')
    def put_sip_buddy(ctx, sip_buddy):
        return deferToThread(SipBuddyDal(ctx).put_sip_buddy, sip_buddy) \
            .addCallback(lambda ret: ctx.transport.respond(HTTP_302,
                                      location="get_sip_buddy?id=%d" %
                                               ret.id))
