from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Device
from .serializers import (
    RegisterSerializer, LoginSerializer,
    GenerateCodeSerializer, ActivateDeviceSerializer
)

class RegisterView(generics.CreateAPIView):
    serializer_class    = RegisterSerializer
    permission_classes  = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class   = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user      = ser.validated_data['user']
        dev_uid   = ser.validated_data['device_id']

        # سجّل الجهاز إن لم يكن موجوداً
        device, created = Device.objects.get_or_create(
            user=user, device_id=dev_uid
        )
        # لا نفعّل هنا: الانتظار حتى Activation

        # إرجاع توكن JWT مع بيانات الجهاز
        refresh = RefreshToken.for_user(user)
        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'device': {
                'device_id': str(device.device_id),
                'code':      device.code,
                'is_active': device.is_active
            }
        }, status=status.HTTP_200_OK)

class GenerateCodeView(generics.CreateAPIView):
    serializer_class   = GenerateCodeSerializer
    permission_classes = [permissions.IsAdminUser]

class ActivateDeviceView(generics.GenericAPIView):
    serializer_class   = ActivateDeviceSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        device = ser.validated_data['device']
        device.is_active = True
        device.save()
        return Response({'detail':'تم تفعيل الجهاز'}, status=status.HTTP_200_OK)
