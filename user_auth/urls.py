from django.urls import path
from .views import *
from rest_framework_simplejwt import views

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', UserLoginView.as_view(), name='login'),
]