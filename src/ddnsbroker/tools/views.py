"""
The functions basic_challenge and basic_authenticate are licensed under the
3-clause BSD license (also known as "Revised BSD License", "New BSD License",
or "Modified BSD License"):

Copyright (c) 2013-2020, The nsupdate.info Development Team (see AUTHORS file)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of nsupdate.info nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import base64

from django.http import HttpResponse


class PlainResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'text/plain'
        super().__init__(*args, **kwargs)


def basic_challenge(realm, content='Authorization Required'):
    """
    Construct a 401 response requesting http basic auth.
    :param realm: realm string (displayed by the browser)
    :param content: request body content
    :return: HttpResponse object
    """
    response = PlainResponse(content)
    response['WWW-Authenticate'] = 'Basic realm="%s"' % (realm,)
    response.status_code = 401
    return response


def basic_authenticate(auth):
    """
    Get username and password from http basic auth string.
    :param auth: http basic auth string [str on py2, str on py3]
    :return: username, password [unicode on py2, str on py3]
    """
    assert isinstance(auth, str)
    try:
        authmeth, auth = auth.split(' ', 1)
    except ValueError:
        # splitting failed, invalid auth string
        return
    if authmeth.lower() != 'basic':
        return
    # we ignore bytes that do not decode. username (hostname) and password
    # (update secret) both have to be ascii, everything else is a configuration
    # error on user side.
    auth = base64.b64decode(auth.strip()).decode('utf-8', errors='ignore')
    username, password = auth.split(':', 1)
    return username, password
