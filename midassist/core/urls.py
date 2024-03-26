from django.urls import path
from .views import your_view
from . import views


urlpatterns = [
    path('your-endpoint/', your_view, name='your_view'),
    path('testDB/', views.testdb),
    path('testDB/<str:pk>/', views.testdb_one),
    path('createValue/', views.create_value),
    path('testDB/<str:pk>/update', views.update_value),
    path('testDB/<str:pk>/delete', views.delete_value),
]
