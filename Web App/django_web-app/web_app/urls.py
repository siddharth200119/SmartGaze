from django.urls import path, include
from .views import *
urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('home/', home, name='home'),
]
