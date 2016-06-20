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

from twisted.internet.threads import deferToThread

from spyne import rpc

from neurons.form import HtmlForm

from spyne.const.http import HTTP_302

from a2billing_spyne.model import Extensions
from a2billing_spyne.service import ReaderServiceBase, ScreenBase, DalBase

ExtScreen = Extensions.customize(
    prot=HtmlForm(), form_action="put_ext",
    child_attrs_all=dict(
        exc=False,
    ),

    child_attrs=dict(
        id=dict(order=0, write=False),
        exten=dict(order=1),
        priority=dict(order=2),
        app=dict(order=3),
        appdata=dict(order=4),
        context=dict(order=5)
    ),
)


class NewExtScreen(ScreenBase):
    main = ExtScreen


class NewExtDetailScreen(ScreenBase):
    main = ExtScreen


class ExtDal(DalBase):
    def put_ext(self, ext):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            session.add(ext)
            session.commit()
            return ext

    def get_ext(self, ext):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            return session.query(Extensions).filter(Extensions.id ==
                                                    ext.id).one()


class ExtReaderServices(ReaderServiceBase):
    @rpc(Extensions.novalidate_freq(), _returns=NewExtScreen,
                                                             _body_style='bare')
    def new_ext(ctx, ext):
        return NewExtScreen(title="New Extension", main=ext)

    @rpc(Extensions.novalidate_freq(), _returns=NewExtScreen,
                                                             _body_style='bare')
    def get_ext_detail(ctx, ext):
        return deferToThread(ExtDal(ctx).get_ext, ext) \
            .addCallback(lambda ret:
                            NewExtDetailScreen(title="Get Extension", main=ret))


class ExtWriterServices(ReaderServiceBase):
    @rpc(Extensions, _body_style='bare')
    def put_ext(ctx, ext):
        return deferToThread(ExtDal(ctx).put_ext, ext) \
            .addCallback(lambda ret: ctx.transport.respond(HTTP_302,
                                            location="get_ext_detail?id=%d" %
                                                     ret.id))
