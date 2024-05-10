from django.urls import path, include
from .views import *
urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('home/', home, name='home'),
    path('save_todo/', save_todo, name='save_todo'),
    path('save_alarm/', save_alarm, name='save_alarm'),
    path('update_task_status/', update_task_status, name='update_task_status'),
    path('todo_api/<int:userid>', todo_api, name='todo_api'),
    path('alarm_api/<int:userid>', alarm_api, name='alarm_api'),
    path('user_api/<int:userid>', user_api, name='user_api'),
]
