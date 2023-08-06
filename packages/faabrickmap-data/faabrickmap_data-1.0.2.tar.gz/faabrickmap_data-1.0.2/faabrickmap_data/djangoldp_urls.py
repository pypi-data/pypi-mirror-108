from django.conf import settings
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import XLSXExportView

urlpatterns = [
    url(r'^societes/xlsx/$', csrf_exempt(XLSXExportView.as_view()), name='societes-xlsx'),
]