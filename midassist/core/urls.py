"""This module providing  url array of MedAssist"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('sign-up/', views.signup_view, name="signup"),
    path('doctors/', views.doctors_view, name="doctors"),
    path('doctors/', views.post_doctor,name="post_doctor"),
    path('doctors/reviews/', views.get_doctotrs_by_review, name="doctor_reviews"),
    path('sign-in/', views.login_view),
    path('log-out/', views.logout_view),
    path('upload_image/', views.post_image),
    path('users/', views.user_details, name="users"),
    path('upload_pdf/', views.post_pdf),
    path('chat/', views.chat, name="chat"),
    path('chexnet/', views.post_chexnet_image, name="chexnet"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
