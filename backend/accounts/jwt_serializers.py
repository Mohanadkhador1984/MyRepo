from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'phone'

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            phone=phone,
            password=password
        )
        if user is None or not user.is_active:
            raise serializers.ValidationError('رقم الهاتف أو كلمة السر غير صحيحة')
        return super().validate(attrs)
