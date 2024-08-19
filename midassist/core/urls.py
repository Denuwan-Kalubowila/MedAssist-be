"""This module providing  url array of MedAssist"""
from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.signup_view, name="signup"),
    path('doctors/', views.post_doctor,name="post_doctor"),
    path('doctors/', views.doctors_view, name="doctors"),
    path('doctors/reviews/', views.get_doctotrs_by_review, name="doctor_reviews"),
    path('sign-in/', views.login_view),
    path('log-out/', views.logout_view),
    path('upload_image/', views.post_image),
    path('users/', views.user_details, name="users"),
    path('upload_pdf/', views.post_pdf),
    # path('chat/', views.chat, name="chat"),
]
