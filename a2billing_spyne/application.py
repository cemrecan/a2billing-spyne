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

import logging
logger = logging.getLogger(__name__)

from os.path import abspath

from twisted.internet import reactor

from spyne.protocol.html import HtmlMicroFormat
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.protocol.xml import XmlDocument

from neurons import Application

from neurons.daemon.config import StaticFileServer, HttpListener

from a2billing_spyne.service import TestServices
from a2billing_spyne.service.card import CardReaderServices, CardWriterServices
from a2billing_spyne.service.sip_buddies import SipReaderServices, SipWriterServices
from a2billing_spyne.service.extensions import ExtReaderServices, ExtWriterServices


def start_a2bs(config):
    subconfig = config.services.getwrite('web', HttpListener(
        host='0.0.0.0',
        port=9271,
        disabled=False,
        _subapps=[
            StaticFileServer(
                url='assets', path=abspath('assets'),
                list_contents=False
            )
        ],
    ))

    services = [
        TestServices,
        CardReaderServices, CardWriterServices,
        SipReaderServices, SipWriterServices,
        ExtReaderServices, ExtWriterServices,

    ]

    subconfig.subapps['json'] = \
        Application(services,
            tns='a2bs.web', name='A2BillingJson',
            in_protocol=HttpRpc(validator='soft'),
            out_protocol=JsonDocument(),
            config=config,
        )

    subconfig.subapps['xml'] = \
        Application(services,
            tns='a2bs.web', name='A2BillingXml',
            in_protocol=HttpRpc(validator='soft'),
            out_protocol=XmlDocument(),
            config=config,
        )

    subconfig.subapps[''] = \
        Application(services,
            tns='a2bs.web', name='A2BillingHtml',
            in_protocol=HttpRpc(validator='soft'),
            out_protocol=HtmlMicroFormat(),
            config=config,
        )

    site = subconfig.gen_site()

    logger.info("listening for a2billing http endpoint %s:%d",
                                                 subconfig.host, subconfig.port)
    return reactor.listenTCP(subconfig.port, site, interface=subconfig.host), None
