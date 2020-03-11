"""
ddnsbroker URL Configuration
"""
from django.contrib import admin
from django.urls import path

from ddnsbroker.views import *

urlpatterns = [
    path('', RemoteIpView.as_view()),
    path('myip', RemoteIpView.as_view()),
    path('nic/update', NicUpdateView.as_view()),
    path('updateservice/<int:id>/get/usernameisfqdn', UpdateServiceGetUsernameIsFqdnView.as_view()),
    path('admin/', admin.site.urls),
]
