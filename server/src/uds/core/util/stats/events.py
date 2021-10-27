# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2021 Virtual Cable S.L.U.
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
import datetime
import logging
import typing

from uds.core.managers.stats import StatsManager
from uds.models import Provider, Service, ServicePool, Authenticator

logger = logging.getLogger(__name__)

EventTupleType = typing.Tuple[datetime.datetime, str, str, str, str, int]
EventClass = typing.Union[Provider, Service, ServicePool, Authenticator]

if typing.TYPE_CHECKING:
    from django.db.models import Model

# Posible events, note that not all are used by every possible owner type
(
    # Login - logout
    ET_LOGIN,
    ET_LOGOUT,
    # Service access
    ET_ACCESS,
    # Cache performance
    ET_CACHE_HIT,
    ET_CACHE_MISS,
    # Platforms detected
    ET_PLATFORM,
    # Tunnel
    ET_TUNNEL_OPEN,
    ET_TUNNEL_CLOSE,
) = range(8)

(
    OT_PROVIDER,
    OT_SERVICE,
    OT_DEPLOYED,
    OT_AUTHENTICATOR,
) = range(4)

__transDict: typing.Mapping[typing.Type['Model'], int] = {
    ServicePool: OT_DEPLOYED,
    Service: OT_SERVICE,
    Provider: OT_PROVIDER,
    Authenticator: OT_AUTHENTICATOR,
}

# Events data (fld1, fld2, fld3, fld4):
# ET_LOGIN --> on Authenticator
#     (username, srcip)
#   Note: Generated on user login on UDS web
#
# ET_PLATFORM --> on Authenticator
#     (platform, browser, version)
#   Note: Generated on user login on UDS web
#
# ET_LOGOUT --> on Authenticator
#     (username, srcip)
#   Note: Generated on user logout on UDS web. Not generated if browser is closed or session discards.
#
# ET_CACHE_HIT --> On UserService
#     (usableServicesInCacheL1,)
#   Note: Generated on assigning from cache to user
#
# ET_CACHE_MISS --> On UserService
#     (preparingServicesInCacheL1,)
#   Note: Generated on missed assigning from cache to user
#
# ET_ACCESS -> On ServicePool
#     (username, srcpi, dstip, userService_uuid)
#   Note: Generated on user access to service in UDS (that is, clicked on an service)
#
# ET_LOGIN -> On ServicePool
#     (username, knownUserIp, serviceIp, fullUserName)
#   Note: Generated by OsManager (that is, services without os manager will not trigger this)
#
# ET_LOGOUT -> On ServicePool
#     (username, knownUserIp, serviceIp, fullUserName)
#   Note: Generated by OsManager (that is, services without os manager will not trigger this)
#
# OT_TUNNEL_OPEN: -> On ServicePool
#     (username, srcip, dstip, tunnel_id)
#   Note: For HTML5, scrip = "source" string indicating tunnel type (HTML5-{RDP,RDP,VNC})
#
# OT_TUNNEL_CLOSE: -> On ServicePool
#     (duration, sent, received, tunnel_id)


def addEvent(obj: EventClass, eventType: int, **kwargs) -> bool:
    """
    Adds a event stat to specified object

    Although any counter type can be added to any object, there is a relation that must be observed
    or, otherway, the stats will not be recoverable at all:


    note: Runtime checks are done so if we try to insert an unssuported stat, this won't be inserted and it will be logged
    """

    return StatsManager.manager().addEvent(
        __transDict[type(obj)], obj.id, eventType, **kwargs
    )


def getEvents(
    obj: EventClass, eventType: int, **kwargs
) -> typing.Generator[EventTupleType, None, None]:
    """
    Get events

    Args:
        obj: Obj for which to recover stats counters
        counterType: type of counter to recover
        since: (optional, defaults to 'Since beginning') Start date for counters to recover
        to: (optional, defaults to 'Until end') En date for counter to recover
        limit: (optional, defaults to 1000) Number of counter to recover. This is an 'At most' advice. The returned number of value
               can be lower, or even 1 more than requested due to a division for retrieving object at database
        all: (optinal), indicates that get all counters for the type of obj passed in, not only for that obj.

    Returns:
        A generator, that contains pairs of (stamp, value) tuples
    """
    from uds.models import NEVER_UNIX, getSqlDatetimeAsUnix

    since = kwargs.get('since', NEVER_UNIX)
    to = kwargs.get('to', getSqlDatetimeAsUnix())
    type_ = type(obj)

    if kwargs.get('all', False):
        owner_id = None
    else:
        owner_id = obj.pk

    for i in StatsManager.manager().getEvents(
        __transDict[type_], eventType, owner_id=owner_id, since=since, to=to
    ):
        yield (
            datetime.datetime.fromtimestamp(i.stamp),
            i.fld1,
            i.fld2,
            i.fld3,
            i.fld4,
            i.event_type,
        )
