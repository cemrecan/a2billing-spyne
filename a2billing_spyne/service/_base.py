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

from lxml.html.builder import E

from spyne import rpc, Unicode, ComplexModel, AnyHtml

from neurons.base.service import TReaderServiceBase
from neurons.base.service import TWriterServiceBase
from neurons.log.model import TLogEntry

from a2billing_spyne.const import T_INDEX

LogEntry = TLogEntry()
ReaderServiceBase = TReaderServiceBase(LogEntry)
WriterServiceBase = TWriterServiceBase(LogEntry)


class ScreenBase(ComplexModel):
    class Attributes(ComplexModel.Attributes):
        html_cloth = T_INDEX

    title = Unicode


class DalBase(object):
    def __init__(self, ctx):
        self.ctx = ctx


class TestServices(ReaderServiceBase):
    @rpc(_in_message_name="", _returns=AnyHtml)
    def index(self):
        return E.div(
            E.p(E.a("Cards", href="/get_all_card")),
            E.p(E.a("Sip Buddies", href="/get_all_sip_buddy")),
            E.p(E.a("Extensions", href="/get_all_extension")),
        )
