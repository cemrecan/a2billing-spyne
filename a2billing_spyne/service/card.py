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
from spyne.protocol.html.table import HtmlColumnTable

from neurons.form import HtmlForm, HrefWidget

from a2billing_spyne.model import Card
from a2billing_spyne.service import ReaderServiceBase, ScreenBase, DalBase


class NewCardScreen(ScreenBase):
    main = Card.customize(
        prot=HtmlForm(), form_action="put_card",
        child_attrs=dict(
            id=dict(exc=True),
        ),
    )


class CardDetailScreen(ScreenBase):
    main = Card.customize(
        prot=HtmlForm(), form_action="put_card",
        child_attrs=dict(
            id=dict(write=False),
        ),
    )


def _write_new_card_link(ctx, cls, inst, parent, name, *kwargs):
    parent.write(E.a("New Card", href="/new_card"))


class CardListScreen(ScreenBase):
    main = Array(
        Card.customize(
            child_attrs=dict(
                id=dict(prot=HrefWidget("/get_card?id={}")),
            ),
        ),
        prot=HtmlColumnTable(before_table=_write_new_card_link),
    )


class CardDal(DalBase):
    def put_card(self, card):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            session.add(card)
            session.commit()

    def get_card(self, card):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            return session.query(Card).filter_by(id=card.id).one()

    def get_all_card(self, card):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            return session.query(Card).all()


class CardReaderServices(ReaderServiceBase):
    @rpc(Card, _returns=NewCardScreen, _body_style='bare')
    def new_card(ctx, card):
        return NewCardScreen(title="Echo Card", main=card)

    @rpc(Card, _returns=CardDetailScreen, _body_style='bare')
    def get_card(ctx, card):
        return deferToThread(CardDal(ctx).get_card, card) \
            .addCallback(lambda ret:
                                   CardDetailScreen(title="Get Card", main=ret))

    @rpc(Card, _returns=CardListScreen, _body_style='bare')
    def get_all_card(ctx, card):
        return deferToThread(CardDal(ctx).get_all_card, card) \
            .addCallback(lambda ret: CardListScreen(title="Cards", main=ret))


class CardWriterServices(ReaderServiceBase):
    @rpc(Card, _body_style='bare')
    def put_card(ctx, card):
        return deferToThread(CardDal(ctx).put_card, card)
