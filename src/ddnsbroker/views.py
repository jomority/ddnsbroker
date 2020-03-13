from django.http import HttpResponse
from django.views.generic import View


class RemoteIpView(View):
    def get(self, request):
        return HttpResponse(request.META.get('REMOTE_ADDR'))


class NicUpdateView(View):
    pass  # TODO
