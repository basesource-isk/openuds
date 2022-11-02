# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Virtual Cable S.L.U.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#    * Neither the name of Virtual Cable S.L. nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
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
"""
@author: Adolfo Gómez, dkmaster at dkmon dot com
"""

import typing
import re
import logging

from django.utils.translation import gettext_noop as _, gettext
import requests
import requests.auth

from uds import models
from uds.core import mfas
from uds.core.ui import gui
from uds.core.util import net

if typing.TYPE_CHECKING:
    from uds.core.module import Module
    from uds.core.util.request import ExtendedHttpRequest

logger = logging.getLogger(__name__)


class SMSMFA(mfas.MFA):
    typeName = _('SMS Thought HTTP')
    typeType = 'smsHttpMFA'
    typeDescription = _('Simple SMS sending MFA using HTTP')
    iconFile = 'sms.png'

    sendingUrl = gui.TextField(
        length=128,
        label=_('URL pattern for SMS sending'),
        order=1,
        tooltip=_(
            'URL pattern for SMS sending. It can contain the following '
            'variables:\n'
            '* {code} - the code to send\n'
            '* {phone/+phone} - the phone number\n'
            '* {username} - the username\n'
            '* {justUsername} - the username without @....'
        ),
        required=True,
        tab=_('HTTP Server'),
    )

    ignoreCertificateErrors = gui.CheckBoxField(
        label=_('Ignore certificate errors'),
        order=2,
        defvalue=False,
        tooltip=_(
            'If checked, the server certificate will be ignored. This is '
            'useful if the server uses a self-signed certificate.'
        ),
        tab=_('HTTP Server'),
    )

    sendingMethod = gui.ChoiceField(
        label=_('SMS sending method'),
        order=3,
        tooltip=_('Method for sending SMS'),
        required=True,
        values=('GET', 'POST', 'PUT'),
        tab=_('HTTP Server'),
    )

    headersParameters = gui.TextField(
        length=4096,
        multiline=4,
        label=_('Headers for SMS requests'),
        order=4,
        tooltip=_(
            'Headers for SMS requests. It can contain the following '
            'variables:\n'
            '* {code} - the code to send\n'
            '* {phone/+phone} - the phone number\n'
            '* {username} - the username\n'
            '* {justUsername} - the username without @....\n'
            'Headers are in the form of "Header: Value". (without the quotes)'
        ),
        required=False,
        tab=_('HTTP Server'),
    )

    sendingParameters = gui.TextField(
        length=4096,
        multiline=5,
        label=_('Parameters for SMS POST/PUT sending'),
        order=4,
        tooltip=_(
            'Parameters for SMS sending via POST/PUT. It can contain the following '
            'variables:\n'
            '* {code} - the code to send\n'
            '* {phone/+phone} - the phone number\n'
            '* {username} - the username\n'
            '* {justUsername} - the username without @....'
        ),
        required=False,
        tab=_('HTTP Server'),
    )

    encoding = gui.ChoiceField(
        label=_('SMS encoding'),
        defaultValue='utf-8',
        order=5,
        tooltip=_('Encoding for SMS'),
        required=True,
        values=('utf-8', 'iso-8859-1'),
        tab=_('HTTP Server'),
    )

    authenticationMethod = gui.ChoiceField(
        label=_('SMS authentication method'),
        order=20,
        tooltip=_('Method for sending SMS'),
        required=True,
        values={
            '0': _('None'),
            '1': _('HTTP Basic Auth'),
            '2': _('HTTP Digest Auth'),
        },
        tab=_('HTTP Authentication'),
    )

    authenticationUserOrToken = gui.TextField(
        length=256,
        label=_('SMS authentication user or token'),
        order=21,
        tooltip=_('User or token for SMS authentication'),
        required=False,
        tab=_('HTTP Authentication'),
    )

    authenticationPassword = gui.PasswordField(
        length=256,
        label=_('SMS authentication password'),
        order=22,
        tooltip=_('Password for SMS authentication'),
        required=False,
        tab=_('HTTP Authentication'),
    )

    responseOkRegex = gui.TextField(
        length=256,
        label=_('SMS response OK regex'),
        order=30,
        tooltip=_(
            'Regex for SMS response OK. If empty, the response is considered OK if status code is 200.'
        ),
        required=False,
        tab=_('HTTP Response'),
    )

    responseErrorAction = gui.ChoiceField(
        label=_('SMS response error action'),
        order=31,
        defaultValue='0',
        tooltip=_('Action for SMS response error'),
        required=True,
        values={
            '0': _('Allow user login'),
            '1': _('Deny user login'),
            '2': _('Allow user to login if it IP is in the networks list'),
            '3': _('Deny user to login if it IP is in the networks list'),
        },
        tab=_('Config'),
    )

    allowLoginWithoutMFA = gui.ChoiceField(
        label=_('User without MFA policy'),
        order=33,
        defaultValue='0',
        tooltip=_('Action for SMS response error'),
        required=True,
        values={
            '0': _('Allow user login'),
            '1': _('Deny user login'),
            '2': _('Allow user to login if it IP is in the networks list'),
            '3': _('Deny user to login if it IP is in the networks list'),
        },
        tab=_('Config'),
    )

    networks = gui.MultiChoiceField(
        label=_('SMS networks'),
        rdonly=False,
        rows=5,
        order=32,
        tooltip=_('Networks for SMS authentication'),
        required=False,
        tab=_('Config'),
    )

    def initialize(self, values: 'Module.ValuesType') -> None:
        return super().initialize(values)

    @classmethod
    def initClassGui(cls) -> None:
        # Populate the networks list
        cls.networks.setValues([
            gui.choiceItem(v.uuid, v.name)
            for v in models.Network.objects.all().order_by('name')
            if v.uuid
        ])

    def composeSmsUrl(self, userId: str, userName: str, code: str, phone: str) -> str:
        url = self.sendingUrl.value
        url = url.replace('{code}', code)
        url = url.replace('{phone}', phone.replace('+', ''))
        url = url.replace('{+phone}', phone)
        url = url.replace('{username}', userName)
        url = url.replace('{justUsername}', userName.split('@')[0])
        return url

    def getSession(self) -> requests.Session:
        session = requests.Session()
        # 0 means no authentication
        if self.authenticationMethod.value == '1':
            session.auth = requests.auth.HTTPBasicAuth(
                username=self.authenticationUserOrToken.value,
                password=self.authenticationPassword.value,
            )
        elif self.authenticationMethod.value == '2':
            session.auth = requests.auth.HTTPDigestAuth(
                self.authenticationUserOrToken.value,
                self.authenticationPassword.value,
            )
        # Any other value means no authentication

        # If set ignoreCertificateErrors, do it
        if self.ignoreCertificateErrors.isTrue():
            session.verify = False
        
        # Add headers. Headers are in the form of "Header: Value". (without the quotes)
        if self.headersParameters.value.strip():
            for header in self.headersParameters.value.split('\n'):
                if header.strip():
                    headerName, headerValue = header.split(':', 1)
                    session.headers[headerName.strip()] = headerValue.strip()
        return session


    def checkAction(self, action: str, request: 'ExtendedHttpRequest') -> bool:
        def checkIp() -> bool:
            return any(i.ipInNetwork(request.ip) for i in models.Network.objects.filter(uuid__in = self.networks.value))

        if action == '0':
            return True
        elif action == '1':
            return False
        elif action == '2':
            return checkIp()
        elif action == '3':
            return not checkIp()
        else:
            return False

    def emptyIndentifierAllowedToLogin(self, request: 'ExtendedHttpRequest') -> bool:
        return self.checkAction(self.allowLoginWithoutMFA.value, request)

    def processResponse(self, request: 'ExtendedHttpRequest', response: requests.Response) -> mfas.MFA.RESULT:
        logger.debug('Response: %s', response)
        if not response.ok:
            if self.responseErrorAction.value == '1':
                raise Exception(_('SMS sending failed'))
        elif self.responseOkRegex.value.strip():
            logger.debug('Checking response OK regex: %s: (%s)', self.responseOkRegex.value, re.search(self.responseOkRegex.value, response.text))
            if not re.search(self.responseOkRegex.value, response.text or ''):
                logger.error(
                    'SMS response error: %s',
                    response.text,
                )
                if not self.checkAction(self.responseErrorAction.value, request):
                    raise Exception(_('SMS response error'))
                return mfas.MFA.RESULT.ALLOWED
        return mfas.MFA.RESULT.OK

    def getData(
        self, request: 'ExtendedHttpRequest', userId: str, username: str, url: str, code: str, phone: str
    ) -> bytes:
        data = ''
        if self.sendingParameters.value:
            data = (
                self.sendingParameters.value.replace('{code}', code)
                .replace('{phone}', phone.replace('+', ''))
                .replace('{+phone}', phone)
                .replace('{username}', username)
                .replace('{justUsername}', username.split('@')[0])
            )
        return data.encode(self.encoding.value)

    def sendSMS_GET(self, request: 'ExtendedHttpRequest', userId: str, username: str, url: str) -> mfas.MFA.RESULT:
        return self.processResponse(request, self.getSession().get(url))

    def sendSMS_POST(
        self, request: 'ExtendedHttpRequest', userId: str, username: str, url: str, code: str, phone: str
    ) -> mfas.MFA.RESULT:
        # Compose POST data
        session = self.getSession()
        bdata = self.getData(request, userId, username, url, code, phone)
        # Add content-length header
        session.headers['Content-Length'] = str(len(bdata))

        return self.processResponse(request, session.post(url, data=bdata))

    def sendSMS_PUT(
        self, request: 'ExtendedHttpRequest', userId: str, username: str, url: str, code: str, phone: str
    ) -> mfas.MFA.RESULT:
        # Compose POST data
        data = ''
        bdata = self.getData(request, userId, username, url, code, phone)
        return self.processResponse(request, self.getSession().put(url, data=bdata))

    def sendSMS(
        self, request: 'ExtendedHttpRequest', userId: str, username: str, code: str, phone: str
    ) -> mfas.MFA.RESULT:
        url = self.composeSmsUrl(userId, username, code, phone)
        if self.sendingMethod.value == 'GET':
            return self.sendSMS_GET(request, userId, username, url)
        elif self.sendingMethod.value == 'POST':
            return self.sendSMS_POST(request, userId, username, url, code, phone)
        elif self.sendingMethod.value == 'PUT':
            return self.sendSMS_PUT(request, userId, username, url, code, phone)
        else:
            raise Exception('Unknown SMS sending method')

    def label(self) -> str:
        return gettext('MFA Code')

    def html(self, request: 'ExtendedHttpRequest') -> str:
        return gettext('Check your phone. You will receive an SMS with the verification code')

    def sendCode(self, request: 'ExtendedHttpRequest', userId: str, username: str, identifier: str, code: str) -> mfas.MFA.RESULT:
        logger.debug(
            'Sending SMS code "%s" for user %s (userId="%s", identifier="%s")',
            code,
            username,
            userId,
            identifier,
        )
        return self.sendSMS(request, userId, username, code, identifier)