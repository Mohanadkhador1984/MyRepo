from django.urls import path
from .views import (
    RegisterView, LoginView,
    GenerateCodeView, ActivateDeviceView
)

app_name = 'accounts'

urlpatterns = [
    path('register/',      RegisterView.as_view(),       name='register'),
    path('login/',         LoginView.as_view(),          name='login'),
    path('generate-code/', GenerateCodeView.as_view(),   name='generate-code'),
    path('activate/',      ActivateDeviceView.as_view(), name='activate'),
]
