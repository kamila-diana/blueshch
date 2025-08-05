from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='welcoming page'),
    path('login/', views.login, name='spotify_login'),
    path('callback/', views.callback, name='spotify_callback'),
    path('play/', views.play, name='spotify_play'),
    path('devices/', views.devices, name='spotify_devices'),
    path('search/', views.search, name='search'),
    path('search_api/', views.search_api, name='search_api'),
]