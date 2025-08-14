# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Device, gen_device_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone    = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get('phone'),
            password=attrs.get('password')
        )
        if not user:
            raise serializers.ValidationError("رقم الهاتف أو كلمة السر خاطئة")
        attrs['user'] = user
        return attrs


class GenerateCodeSerializer(serializers.Serializer):
    device_id = serializers.UUIDField()

    def validate_device_id(self, value):
        if not Device.objects.filter(device_id=value).exists():
            raise serializers.ValidationError("الجهاز غير مسجّل")
        return value

    def create(self, validated_data):
        device = Device.objects.get(device_id=validated_data['device_id'])
        device.code = gen_device_code()
        device.save()
        return {'code': device.code}


class ActivateDeviceSerializer(serializers.Serializer):
    device_id = serializers.UUIDField()
    code      = serializers.CharField()

    def validate(self, attrs):
        try:
            device = Device.objects.get(device_id=attrs['device_id'])
        except Device.DoesNotExist:
            raise serializers.ValidationError("الجهاز غير مسجّل")

        if device.code != attrs['code']:
            raise serializers.ValidationError("رمز التفعيل غير صحيح")

        attrs['device'] = device
        return attrs

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.save()
        return instance
