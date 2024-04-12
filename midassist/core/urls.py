"""This module providing  url array of MedAssist"""
from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.signup_view),
    path('sign-in/', views.login_view),
    path('log-out/', views.logout_view),
    path('upload_image/', views.post_image),

]
