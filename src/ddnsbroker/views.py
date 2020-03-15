from django.http import HttpResponse
from django.views.generic import View

from ddnsbroker.tools import normalize_ip


class PlainResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'text/plain'
        super().__init__(*args, **kwargs)


class RemoteIpView(View):
    def get(self, request):
        return PlainResponse(normalize_ip(request.META.get('REMOTE_ADDR')))


class NicUpdateView(View):
    pass  # TODO
