from django.urls import path, include
from .views import *


urlpatterns = [
    path('', login, name='login'),
    path('trial', trial, name='trial'),
]