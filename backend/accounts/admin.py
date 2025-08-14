# backend/accounts/admin.py
from django.contrib import admin
from .models import CustomUser, Device

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'is_staff', 'is_active')
    search_fields = ('phone',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_id', 'code', 'is_active', 'last_used')
    list_filter = ('is_active',)
    search_fields = ('device_id', 'code', 'user__phone')
