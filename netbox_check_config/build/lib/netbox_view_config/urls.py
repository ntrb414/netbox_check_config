from django.urls import path
from .views import DeviceConfigView

urlpatterns = [
    path('device/<int:pk>/config/', DeviceConfigView.as_view(), name='device_config'),
]
