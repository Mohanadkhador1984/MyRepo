from django.urls import path
from .views import  PhoneTokenObtainView, PhoneTokenRefreshView


app_name = 'accounts'

urlpatterns = [
  # path('signup/', RegisterView.as_view(), name='signup'),
  path('login/',  PhoneTokenObtainView.as_view(), name='login'),
  path('refresh/', PhoneTokenRefreshView.as_view(), name='refresh'),
]
