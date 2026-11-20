from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('team/', views.team, name='team'),
    path('properties/', views.property_search, name='property_search'),
    path('property/<int:pk>/', views.property_detail, name='public_property_detail'),
]
