# -*- coding: utf-8 -*-

#
# Copyright (c) 2012-2021 Virtual Cable S.L.U.
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
#    * Neither the name of Virtual Cable S.L.U. nor the names of its contributors
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
import functools
import logging
import inspect
import typing
import threading

if typing.TYPE_CHECKING:
    from uds.core.util.cache import Cache


logger = logging.getLogger(__name__)

RT = typing.TypeVar('RT')

def _defaultDenyView(request) -> typing.Any:
    from uds.web.util import errors
    return errors.errorView(
        request, errors.BROWSER_NOT_SUPPORTED
    )

# Decorator that protects pages that needs at least a browser version
# Default is to deny IE < 9
def denyBrowsers(
    browsers: typing.Optional[typing.List[str]] = None,
    errorResponse: typing.Callable = _defaultDenyView,
) -> typing.Callable[[typing.Callable[..., RT]], typing.Callable[..., RT]]:
    """
    Decorator to set protection to access page
    Look for samples at uds.core.web.views
    """
    from uds.core.util.html import checkBrowser

    denied: typing.List[str] = browsers or ['ie<9']

    def wrap(view_func: typing.Callable[..., RT]) -> typing.Callable[..., RT]:
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs) -> RT:
            """
            Wrapped function for decorator
            """
            for b in denied:
                if checkBrowser(request, b):
                    return errorResponse(request)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return wrap


def deprecated(func: typing.Callable[..., RT]) -> typing.Callable[..., RT]:
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs) -> RT:
        try:
            caller = inspect.stack()[1]
            logger.warning(
                'Call to deprecated function %s from %s:%s.',
                func.__name__,
                caller[1],
                caller[2],
            )
        except Exception:
            logger.info('No stack info on deprecated function call %s', func.__name__)

        return func(*args, **kwargs)

    return new_func

def deprecatedClassValue(newVarName: str) -> typing.Callable:
    class innerDeprecated:
        fget: typing.Callable
        new_var_name: str

        def __init__(self, method: typing.Callable, newVarName: str) -> None:
            self.new_var_name = newVarName
            self.fget = method  # type: ignore

        def __get__(self, instance, cls=None):
            try:
                caller = inspect.stack()[1]
                logger.warning(
                    'Use of deprecated class value %s from %s:%s. Use %s instead.',
                    self.fget.__name__,
                    caller[1],
                    caller[2],
                    self.new_var_name,
                )
            except Exception:
                logger.info('No stack info on deprecated value use %s', self.fget.__name__)

            return self.fget(cls)

    return functools.partial(innerDeprecated, newVarName=newVarName)


def ensureConected(func: typing.Callable[..., RT]) -> typing.Callable[..., RT]:
    """This decorator calls "connect" method of the class of the wrapped object"""

    @functools.wraps(func)
    def new_func(*args, **kwargs) -> RT:
        args[0].connect()
        return func(*args, **kwargs)

    return new_func


# Decorator that allows us a "fast&clean" caching system on service providers
#
# Decorator for caching
# Decorator that tries to get from cache before executing
def allowCache(
    cachePrefix: str,
    cacheTimeout: typing.Union[typing.Callable[[], int], int] = -1,
    cachingArgs: typing.Optional[
        typing.Union[typing.List[int], typing.Tuple[int], int]
    ] = None,
    cachingKWArgs: typing.Optional[
        typing.Union[typing.List[str], typing.Tuple[str], str]
    ] = None,
    cachingKeyFnc: typing.Optional[typing.Callable[[typing.Any], str]] = None,
) -> typing.Callable[[typing.Callable[..., RT]], typing.Callable[..., RT]]:
    """Decorator that give us a "quick& clean" caching feature.
    The "cached" element must provide a "cache" variable, which is a cache object

    :param cachePrefix: the cache key "prefix" (prepended on generated key from args)
    :param cacheTimeout: The cache timeout in seconds
    :param cachingArgs: The caching args. Can be a single integer or a list.
                        First arg (self) is 0, so normally cachingArgs are 1, or [1,2,..]
    :param cachingKWArgs: The caching kwargs. Can be a single string or a list.
    :param cachingKeyFnc: A function that receives the args and kwargs and returns the key
    """
    cacheTimeout = Cache.DEFAULT_VALIDITY if cacheTimeout == -1 else cacheTimeout
    keyFnc = cachingKeyFnc or (lambda x: '')

    def allowCacheDecorator(fnc: typing.Callable[..., RT]) -> typing.Callable[..., RT]:
        @functools.wraps(fnc)
        def wrapper(*args, **kwargs) -> RT:
            argList: typing.List[str] = []
            if cachingArgs:
                ar = (
                    [cachingArgs]
                    if not isinstance(cachingArgs, (list, tuple))
                    else cachingArgs
                )
                argList = [args[i] if i < len(args) else '' for i in ar]

            if cachingKWArgs:
                kw = (
                    [cachingKWArgs]
                    if not isinstance(cachingKWArgs, (list, tuple))
                    else cachingKWArgs
                )
                argList += [str(kwargs.get(i, '')) for i in kw]

            if argList:
                cacheKey = '{}-{}.{}'.format(cachePrefix, keyFnc(args[0]), argList)
            else:
                cacheKey = '{}-{}.gen'.format(cachePrefix, keyFnc(args[0]))

            data: typing.Any = None
            if kwargs.get('force', False) is False and args[0].cache:
                data = args[0].cache.get(cacheKey)
                if data:
                    logger.debug('Cache hit for %s', cacheKey)
                    return data

            if 'force' in kwargs:
                # Remove force key
                del kwargs['force']
                
            # ic cacheTimeout is a function, call it
            timeout = cacheTimeout
            if callable(timeout):
                timeout = timeout()

            if args[0].cache:  # Not in cache and object can cache it
                data = fnc(*args, **kwargs)
                try:
                    # Maybe returned data is not serializable. In that case, cache will fail but no harm is done with this
                    args[0].cache.put(cacheKey, data, timeout)
                except Exception as e:
                    logger.debug(
                        'Data for %s is not serializable on call to %s, not cached. %s (%s)',
                        cacheKey,
                        fnc.__name__,
                        data,
                        e,
                    )
            return data

        return wrapper

    return allowCacheDecorator

# Decorator to execute method in a thread
def threaded(func: typing.Callable[..., None]) -> typing.Callable[..., None]:
    """Decorator to execute method in a thread"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper