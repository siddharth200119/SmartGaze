from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from rest_framework import status
import base64
import json
import requests
import urllib
from urllib.parse import urlencode
from .models import *
from .serializers import *
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
            return redirect('login')
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
            return redirect('login')
    else:  
        form = RegistrationForm()  

    context = {'form': form}
    return render(request, 'register.html', context)


#Function to logout to login page
@login_required()
def user_logout(request):
    logout(request)
    messages.info(request, "Logged Out!")
    return redirect('login')


#Function to view the homepage & view the list of tasks and alarms
@login_required()
def home(request):
    uid = request.user.id
    todoform = TodoListForm()
    alarmform = AlarmForm()
    updateform = StatusUpdateForm(userid=uid)
    uid = request.user
    fname = request.user.first_name
    try:
        tasks = To_do_list.objects.filter(userid=uid)
        alarm = Bridge.objects.filter(userid=uid)
    except To_do_list.DoesNotExist:
        pass
    context = {'todoform': todoform,
               'alarmform': alarmform, 
               'updateform': updateform,
                'tasks': tasks,
                'alarms': alarm,
                'fname': fname}
    return render(request, 'home.html', context)


#Function to view the homepage with all the tasks & add tasks to ToDo List 
@login_required()
def save_todo(request):
    tasks = None
    if request.method == 'POST':
        todoform = TodoListForm(request.POST)
        if todoform.is_valid():  
            title = todoform.cleaned_data['title']
            itemd = todoform.cleaned_data['item_description']
            date = todoform.cleaned_data['due_date']

            uid = request.user
            task = To_do_list(title=title, item_description=itemd, due_date=date, userid=uid)
            task.save()
    return redirect('home')



#Function to set the alarm
@login_required()
def save_alarm(request):
    alarms = None
    if request.method == 'POST':
        alarmform = AlarmForm(request.POST)
        if alarmform.is_valid():  
            atime = alarmform.cleaned_data['alarm_time']
            adate = alarmform.cleaned_data['alarm_date']
            mid = alarmform.cleaned_data['mirrorid']
            uid = request.user
            alarm = Bridge(userid=uid, alarm_date=adate, alarm_time=atime, mirrorid=mid)
            alarm.save()
    return redirect('home')
    # else:
    #     todoform = TodoListForm()
    #     alarmform = AlarmForm()
    #     uid = request.user
    #     try:
    #         tasks = To_do_list.objects.filter(userid=uid)
    #     except To_do_list.DoesNotExist:
    #         pass
    # context = {'todoform': todoform,
    #             'tasks': tasks,
    #            'alarmform': alarmform, 
    #            'alarm': alarm
    #            }
    
    # return render(request, 'home.html', context)


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
                messages.success(request, 'Task status updated successfully.')
            except To_do_list.DoesNotExist:
                messages.error(request, 'Task not found.')
    return redirect('home')


''' API Functions '''


#API to get the tasks of ToDo List
@api_view(["GET"])
def todo_api(request, userid):
    data = To_do_list.objects.filter(userid=userid)
    serializer = ToDoSerializer(data, many=True)
    return Response({
        'data': serializer.data
        })


#API to get the details of the Alarm
@api_view(["GET"])
def alarm_api(request, userid):
    uid = request.user
    data = Bridge.objects.filter(userid=userid)
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


#API to get all the user data, with alarm & todo list details
@api_view(["GET"])
def get_everything_api(request, userid):
    bridge_data = Bridge.objects.filter(userid=userid).first()
    if not bridge_data:
        return Response({'error': 'Mirror not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BridgeSerializer(bridge_data)
    return Response(serializer.data)


#Function to Login to spotify using spotify SDK Endpoints
def spotify_login(request):
    scope = "streaming \
               user-read-email \
               user-read-private"
    auth_query_parameters = {
        "response_type": "code",
        "client_id": 'f9b2ce4da25d46089002cb53895170df',
        "scope": scope,
        "redirect_uri": "http://localhost:8000/spotify/callback",
    }
    authorization_url = 'https://accounts.spotify.com/authorize/?' + urlencode(auth_query_parameters)
    return redirect(authorization_url)


# @login_required()
@api_view(["GET"])
def spotify_callback(request):
    code = request.GET.get('code')
    if code:
        token_url = 'https://accounts.spotify.com/api/token'

        spotify_client_id = 'f9b2ce4da25d46089002cb53895170df'
        spotify_client_secret = '58e3fd6f522c453a83f5e2fd96096b9f'

        redirect_uri = 'http://localhost:8000/spotify/callback'

        form_data = {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        # Encode the client ID and client secret as base64
        auth_header = base64.b64encode(f'{spotify_client_id}:{spotify_client_secret}'.encode()).decode('utf-8')

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Make the POST request to the token endpoint
        response = requests.post(token_url, data=form_data, headers=headers)

        content = json.loads(response.content)
        access_token=content['access_token']
        refresh_token = content['refresh_token']
        uid = request.user.id
        user = Mirror_Users.objects.filter(id=uid).update(spotify_access_token=access_token)

        if response.status_code == 200:
            access_token = response.json()['access_token']
            return redirect('/')
        else:
            # Handle error if the request failed
            return redirect('/error')

    else:
        # Handle error if code parameter is missing
        return redirect('/error')
    return Response(code)


