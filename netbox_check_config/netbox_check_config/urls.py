from django.urls import path
from .views import DeviceConfigView, DeviceConfigAPIView

urlpatterns = [
    path('device/<int:pk>/config/', DeviceConfigView.as_view(), name='device_config'),
    path('device/<int:pk>/config-api/', DeviceConfigAPIView.as_view(), name='device_config_api'),
]
