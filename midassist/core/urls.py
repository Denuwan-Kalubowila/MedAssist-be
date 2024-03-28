"""This module providing  url array of MedAssist"""
from django.urls import path
from .views import your_view
from . import views


urlpatterns = [
    path('your-endpoint/', your_view, name='your_view'),
    path('test-database/', views.testdb),
    path('test-database/<str:pk>/', views.testdb_one),
    path('create-value/', views.create_value),
    path('test-database/<str:pk>/update', views.update_value),
    path('test-database/<str:pk>/delete', views.delete_value),
]
