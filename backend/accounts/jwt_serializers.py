# backend/accounts/jwt_serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    # نجعل authenticate يبحث في حقل 'phone' بدل 'username'
    def validate(self, attrs):
        phone    = attrs.get("phone")
        password = attrs.get("password")

        user = authenticate(username=phone, password=password)
        if not user:
            raise serializers.ValidationError(_("رقم الجوال أو كلمة المرور غير صحيحة"))

        # نمرّر للميراث بيانات صحيحة كي يصدر التوكن
        data = super().validate({
            "username": user.username,
            "password": password,
        })

        # إضافة claim جديدة داخل التوكن
        data["phone"] = user.phone
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # تضمين رقم الجوال داخل payload للتوكن
        token["phone"] = user.phone
        return token
