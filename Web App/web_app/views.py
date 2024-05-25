from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from rest_framework import status
import base64
import json
import requests
from urllib.parse import urlencode
from .models import *
from .serializers import *
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv, find_dotenv
import os
dotenv_path = find_dotenv('../.env')
load_dotenv(dotenv_path)

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
# Create your views here.
User = get_user_model()


#Function to login to a account
def user_login(request):
    if request.method == 'POST':
        usrnm = request.POST.get('username')
        pw = request.POST.get('password')
        user = authenticate(request, username=usrnm, password=pw)
        if user is not None:
            login(request,user)
            messages.success(request, "Logged in!")
            return redirect('home')
        else:
            messages.warning(request, 'Invalid username or password.')
            return redirect('user_login')
    else:
        return render(request, 'login.html')
    

#Function to register a new account
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) 
        if form.is_valid():  
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!')
                return redirect('register')

            if password != re_password:
                messages.info(request, 'Passwords do not match!')
                return redirect('register')

            user = User(username=username, first_name=fname, last_name=lname, email=email, password=make_password(password))
            user.save()

            messages.success(request, 'Account created successfully')  
            return redirect('user_login')
    else:  
        form = RegistrationForm()  

    context = {'form': form}
    return render(request, 'register.html', context)


#Function to logout to login page
@login_required()
def user_logout(request):
    logout(request)
    messages.info(request, "Logged Out!")
    return redirect('user_login')


#Function to view the homepage & view all your details
@login_required()
def home(request):
    uid = request.user.id
    todoform = TodoListForm()
    alarmform = AlarmForm()
    updateform = StatusUpdateForm(userid=uid)
    mirrorform = MirrorForm()
    newsform = NewsForm()
    uid = request.user
    fname = request.user.first_name
    try:
        tasks = To_do_list.objects.filter(userid=uid)
        alarm = Bridge.objects.filter(userid=uid)
        news = News_pref.objects.filter(userid=uid)
    except To_do_list.DoesNotExist:
        pass
    context = {'todoform': todoform,
               'alarmform': alarmform, 
               'updateform': updateform,
               'mirrorform': mirrorform,
               'newsform': newsform,
                'tasks': tasks,
                'alarms': alarm,
                'news': news,
                'fname': fname}
    return render(request, 'home.html', context)


#Function to add tasks to ToDo List 
@login_required()
def save_todo(request):
    task = None
    if request.method == 'POST':
        todoform = TodoListForm(request.POST)
        if todoform.is_valid():  
            title = todoform.cleaned_data['title']
            itemd = todoform.cleaned_data['item_description']
            date = todoform.cleaned_data['due_date']

            uid = request.user
            task = To_do_list(title=title, item_description=itemd, due_date=date, userid=uid)
            task.save()
            messages.success(request, 'Task Created Successfully!')
    return redirect('home')


#Function to set the alarm
@login_required()
def save_alarm(request):
    alarm = None
    if request.method == 'POST':
        alarmform = AlarmForm(request.POST)
        if alarmform.is_valid():  
            atime = alarmform.cleaned_data['alarm_time']
            adate = alarmform.cleaned_data['alarm_date']
            mid = alarmform.cleaned_data['mirrorid']
            uid = request.user
            alarm = Bridge(userid=uid, alarm_date=adate, alarm_time=atime, mirrorid=mid)
            alarm.save()
            messages.success(request, 'Alarm Created Successfully!')
    return redirect('home')


#Function to update the task status in the To-Do List
@login_required()
def update_task_status(request):
    uid = request.user.id
    if request.method == 'POST':
        # form = StatusUpdateForm(request.POST)
        form = StatusUpdateForm(userid=uid, data=request.POST)
        if form.is_valid():
            # tid = form.cleaned_data['tid']
            tid = request.POST.get('tid')
            status = form.cleaned_data['task_status']
            try:
                updated_task = To_do_list.objects.get(tid=tid, userid=uid)
                updated_task.task_status = status   
                updated_task.save()
                messages.success(request, 'Task Status Updated Successfully.')
            except To_do_list.DoesNotExist:
                messages.error(request, 'Task Not Found.')
    return redirect('home')


#Function to add a Mirror to the DB
@login_required()
def add_mirror(request):
    uid = request.user.id
    if request.method == 'POST':
        form = MirrorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['mirror_name']
            mirror = Mirror(mirror_name=name)
            mirror.save()
            messages.success(request, 'Mirror Added successfully.')
    return redirect('home')


#Function to add news preferences of the user
@login_required()
def add_news_pref(request):
    uid = request.user
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # mid = request.POST.get('mid')
            name = form.cleaned_data['topic']
            news = News_pref(topic=name, userid=uid)
            news.save()
            messages.success(request, 'News Topic Added Successfully.')
    return redirect('home')


''''''''''''''''''''''''''''''''''''''''''''''''' API Functions '''''''''''''''''''''''''''''''''''''


#API to get the tasks of ToDo List
# @api_view(["GET"])
# def todo_api(request, userid):
#     data = To_do_list.objects.filter(userid=userid)
#     serializer = ToDoSerializer(data, many=True)
#     return Response({
#         'data': serializer.data
#         })


#API to get the details of the pre-set Alarm of specific Mirror
@api_view(["GET"])
def alarm_api(request, mirrorid):
    uid = request.user
    data = Bridge.objects.filter(mirrorid=mirrorid).order_by('alarm_date', 'alarm_time')
    serializer = AlarmSerializer(data, many=True)
    return Response({
        'data': serializer.data
        })


#API to get the details of the User's face pattern with user ID & username
@api_view(["GET"])
def get_face_patterns_api(request, mirrorid):
    bridge_data = Bridge.objects.filter(mirrorid=mirrorid)
    serialized_data = []

    for bridge_obj in bridge_data:
        user_serializer = UsersSerializer(bridge_obj.userid)
        serialized_data.append({
            'userid': bridge_obj.userid.id,
            'username': user_serializer.data['username'],
            'face_pattern': user_serializer.data['face_pattern']
        })

    return Response({'data': serialized_data})


#API to get all the user's data & refresh the Spotify access token 
@api_view(["GET"])
def get_everything_api(request, userid):
    bridge_data = Bridge.objects.filter(userid=userid).first()
    if not bridge_data:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = get_object_or_404(Mirror_Users, id=userid)
    refresh_token = user.spotify_refresh_token
    uid=request.user.id
    # print(refresh_token)

    client_id = spotify_client_id
    client_secret = spotify_client_secret

    credentials = f"{client_id}:{client_secret}"

    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Basic {encoded_credentials}"
        },
        'data': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    }

    response = requests.post(auth_options['url'], headers=auth_options['headers'], data=auth_options['data'])
    # print(response)

    if response.status_code == 200:
        body = response.json()
        access_token = body.get('access_token')
        new_refresh_token = body.get('refresh_token', refresh_token)  
        
        Mirror_Users.objects.filter(id=uid).update(spotify_access_token=access_token)
        Mirror_Users.objects.filter(id=uid).update(spotify_refresh_token=new_refresh_token)
    else:
        return HttpResponse("ERROR RESPONSE FROM SPOTIFY")
        print('error')

    serializer = BridgeSerializer(bridge_data)

    return Response(serializer.data)


#API to get all the user's spotify access token & refresh token
@api_view(["GET"])
def get_token_api(request, userid):
    user_data = Mirror_Users.objects.filter(id=userid).first()
    if not user_data:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)

    serializer = SpotifySerializer(user_data)
    return Response(serializer.data)


#API to Login to spotify using spotify SDK Endpoints
@api_view(["GET"])
def spotify_login(request):
    scope = "streaming \
               user-read-email \
               user-read-private"
    auth_query_parameters = {
        "response_type": "code",
        "client_id": spotify_client_id,
        "scope": scope,
        "redirect_uri": "http://localhost:8000/spotify/callback"
    }
    authorization_url = 'https://accounts.spotify.com/authorize/?' + urlencode(auth_query_parameters)
    return redirect(authorization_url)


#API to get the access & refresh token by passing the code to the Spotify API Endpoint
@login_required()
@api_view(["GET"])
def spotify_callback(request):
    code = request.GET.get('code')
    if code:
        token_url = 'https://accounts.spotify.com/api/token'

        redirect_uri = 'http://localhost:8000/spotify/callback'

        form_data = {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        auth_header = base64.b64encode(f'{spotify_client_id}:{spotify_client_secret}'.encode()).decode('utf-8')

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded',
            "Access-Control-Allow-Credentials": "true"
        }

        response = requests.post(token_url, data=form_data, headers=headers)

        content = json.loads(response.content)
        access_token=content['access_token']
        refresh_token = content['refresh_token']
        uid = request.user.id
        # print("after spotify", uid)
        Mirror_Users.objects.filter(id=uid).update(spotify_access_token=access_token)
        Mirror_Users.objects.filter(id=uid).update(spotify_refresh_token=refresh_token)

        if response.status_code == 200:
            access_token = response.json()['access_token']
            return redirect('home')
        else:
            return redirect('/error')

    else:
        return redirect('/error')



