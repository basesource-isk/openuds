# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2019 Virtual Cable S.L.
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
.. moduleauthor:: Adolfo Gómez, dkmaster at dkmon dot com
"""
import threading
import datetime
import weakref
import logging
import typing

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from uds.core.util import os_detector as OsDetector
from uds.core.util.tools import DictAsObj
from uds.core.util.config import GlobalConfig
from uds.core.auths.auth import EXPIRY_KEY, ROOT_ID, USER_KEY, getRootUser, webLogout
from uds.models import User

# How often to check the requests cache for stuck objects
CHECK_SECONDS = 3600 * 24  # Once a day is more than enough


class ExtendedHttpRequest(HttpRequest):
    ip: str
    ip_proxy: str
    os: DictAsObj
    user: typing.Optional[User]  # type: ignore   # HttpRequests users "user" for it own, but we redefine it because base is not used...


class ExtendedHttpRequestWithUser(ExtendedHttpRequest):
    user: User


logger = logging.getLogger(__name__)

_requests: typing.Dict[int, typing.Tuple[weakref.ref, datetime.datetime]] = {}


def getIdent() -> int:
    ident = threading.current_thread().ident
    return ident if ident else -1


def getRequest() -> ExtendedHttpRequest:
    ident = getIdent()
    if ident in _requests:
        val = typing.cast(
            typing.Optional[ExtendedHttpRequest], _requests[ident][0]()
        )  # Return obj from weakref
        if val:
            return val

    return ExtendedHttpRequest()


class UDSSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


class GlobalRequestMiddleware:
    lastCheck: typing.ClassVar[datetime.datetime] = datetime.datetime.now()

    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]):
        self._get_response: typing.Callable[[HttpRequest], HttpResponse] = get_response

    def _process_request(self, request: ExtendedHttpRequest) -> None:
        # Store request on cache

        _requests[getIdent()] = (
            weakref.ref(typing.cast(ExtendedHttpRequest, request)),
            datetime.datetime.now(),
        )

        # Add IP to request
        GlobalRequestMiddleware.fillIps(request)
        # Ensures request contains os
        request.os = OsDetector.getOsFromUA(
            request.META.get('HTTP_USER_AGENT', 'Unknown')
        )
        # Ensures that requests contains the valid user
        GlobalRequestMiddleware.getUser(request)

    def _process_response(self, request: ExtendedHttpRequest, response: HttpResponse):
        # Remove IP from global cache (processing responses after this will make global request unavailable,
        # but can be got from request again)
        ident = getIdent()
        logger.debug('Deleting %s', ident)
        try:
            if ident in _requests:
                del _requests[ident]  # Remove stored request
            else:
                logger.info('Request id %s not stored in cache', ident)
        except Exception:
            logger.exception('Deleting stored request')

        # Clean old stored if needed
        GlobalRequestMiddleware.cleanStuckRequests()

        return response

    def __call__(self, request: ExtendedHttpRequest):
        self._process_request(request)

        # Now, check if session is timed out...
        if request.user:
            # return HttpResponse(content='Session Expired', status=403, content_type='text/plain')
            now = timezone.now()
            expiry = request.session.get(EXPIRY_KEY, now)
            if expiry < now:
                webLogout(
                    request=request
                )  # Ignore the response, just processes usere session logout
                return HttpResponse(content='Session Expired', status=403)
            # Update session timeout..self.
            request.session[EXPIRY_KEY] = now + datetime.timedelta(
                seconds=GlobalConfig.SESSION_DURATION_ADMIN.getInt()
                if request.user.isStaff()
                else GlobalConfig.SESSION_DURATION_USER.getInt()
            )

        response = self._get_response(request)

        return self._process_response(request, response)

    @staticmethod
    def cleanStuckRequests() -> None:
        # In case of some exception, keep clean very old request from time to time...
        if (
            GlobalRequestMiddleware.lastCheck
            > datetime.datetime.now() - datetime.timedelta(seconds=CHECK_SECONDS)
        ):
            return
        logger.debug('Cleaning stuck requests from %s', _requests)
        # No request lives 60 seconds, so 60 seconds is fine
        cleanFrom: datetime.datetime = datetime.datetime.now() - datetime.timedelta(
            seconds=60
        )
        toDelete: typing.List[int] = []
        for ident, request in _requests.items():
            if request[1] < cleanFrom:
                toDelete.append(ident)
        for ident in toDelete:
            try:
                del _requests[ident]
            except Exception:
                pass  # Ignore it silently

    @staticmethod
    def fillIps(request: ExtendedHttpRequest):
        """
        Obtains the IP of a Django Request, even behind a proxy

        Returns the obtained IP, that always will be a valid ip address.
        """
        behind_proxy = GlobalConfig.BEHIND_PROXY.getBool(False)
        try:
            request.ip = request.META['REMOTE_ADDR']
        except Exception:
            logger.exception('Request ip not found!!')
            request.ip = ''  # No remote addr?? ...

        try:
            proxies = request.META['HTTP_X_FORWARDED_FOR'].split(",")
            request.ip_proxy = proxies[0]

            if not request.ip or behind_proxy:
                # Request.IP will be None in case of nginx & gunicorn
                # Some load balancers may include "domains" on x-forwarded for,
                request.ip = request.ip_proxy.split('%')[0]  # Stores the ip

                # will raise "list out of range", leaving ip_proxy = proxy in case of no other proxy apart of nginx
                request.ip_proxy = proxies[1].strip()
        except Exception:
            request.ip_proxy = request.ip

    @staticmethod
    def getUser(request: ExtendedHttpRequest) -> None:
        """
        Ensures request user is the correct user
        """
        user_id = request.session.get(USER_KEY)
        user: typing.Optional[User] = None
        if user_id:
            try:
                if user_id == ROOT_ID:
                    user = getRootUser()
                else:
                    user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                user = None

        logger.debug('User at Middleware: %s %s', user_id, user)

        request.user = user
