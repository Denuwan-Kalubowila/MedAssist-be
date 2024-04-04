"""This module providing  url array of MedAssist"""
from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.register_user),
    path('sign-in/', views.user_login),
    path('log-out/', views.user_logout),
]
