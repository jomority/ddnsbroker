from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from ddnsbroker.models import UpdateService


class RemoteIpView(View):
    def get(self, request):
        return HttpResponse(request.META.get('REMOTE_ADDR'))


class NicUpdateView(View):
    pass  # TODO


class UpdateServiceGetUsernameIsFqdnView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            raise PermissionDenied

        try:
            uif = UpdateService.objects.get(id=id).username_is_fqdn
        except UpdateService.DoesNotExist:
            uif = False

        return JsonResponse(uif, safe=False)
