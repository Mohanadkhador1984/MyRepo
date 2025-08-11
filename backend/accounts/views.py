from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from .jwt_serializers import PhoneTokenObtainPairSerializer

User = get_user_model()

@method_decorator(csrf_exempt, name="dispatch")
class PhoneTokenObtainView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

@method_decorator(csrf_exempt, name="dispatch")
class PhoneTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
