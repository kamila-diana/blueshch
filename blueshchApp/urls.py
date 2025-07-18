from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='spotify_login'),
    path('callback/', views.callback, name='spotify_callback'),
    path('play/', views.play, name='spotify_play'),
    path('devices/', views.devices, name='spotify_devices')
]