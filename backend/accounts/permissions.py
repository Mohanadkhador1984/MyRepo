from rest_framework.permissions import BasePermission
from .models import Device

class IsDeviceActive(BasePermission):
    message = 'يرجى تفعيل الجهاز أولاً'

    def has_permission(self, request, view):
        dev_id   = request.headers.get('X-Device-ID')
        is_active = Device.objects.filter(
            device_id=dev_id, is_active=True
        ).exists()
        return bool(is_active)
