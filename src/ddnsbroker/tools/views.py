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
