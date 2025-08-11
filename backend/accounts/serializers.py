from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'password')

    def create(self, validated_data):
        phone = validated_data['phone']
        password = validated_data['password']
        user = User.objects.create_user(
            username=phone,    # نمرر phone كـ username أيضاً
            phone=phone,
            password=password
        )
        return user
