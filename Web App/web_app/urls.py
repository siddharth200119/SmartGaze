from django.urls import path, include
from .views import *
urlpatterns = [
    path('', user_login, name='user_login'),
    path('register/', register, name='register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('home/', home, name='home'),
    path('save_todo/', save_todo, name='save_todo'),
    path('save_alarm/', save_alarm, name='save_alarm'),
    path('update_task_status/', update_task_status, name='update_task_status'),
    path('add_mirror/', add_mirror, name='add_mirror'),
    path('add_news_pref/', add_news_pref, name='add_news_pref'),
    # path('todo_api/<int:userid>', todo_api, name='todo_api'),
    path('alarm_api/<int:mirrorid>', alarm_api, name='alarm_api'),
    path('get_face_patterns_api/<int:mirrorid>', get_face_patterns_api, name='get_face_patterns_api'),
    path('get_everything_api/<int:userid>', get_everything_api, name='get_everything_api'),
    path('get_token_api/<int:userid>', get_token_api, name='get_token_api'),
    path('spotify/login/', spotify_login, name='spotify_login'),
    path('spotify/callback/', spotify_callback, name='spotify/callback/'),
]
