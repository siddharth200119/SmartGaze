"""
    Views for The SmartGaze Web App
"""

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from .forms import *
from dotenv import load_dotenv, find_dotenv
import os
dotenv_path = find_dotenv('../.env')
load_dotenv(dotenv_path)

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
# Create your views here.
User = get_user_model()


def user_login(request):
    """
        To login to a account
    """
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
    

def register(request):
    """"
        To register a new account
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST) 
        if form.is_valid():  
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            mirror = form.cleaned_data['connect_with_mirror']

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!')
                return redirect('register')

            if password != re_password:
                messages.info(request, 'Passwords do not match!')
                return redirect('register')

            user = User(username=username, first_name=fname, last_name=lname, email=email, password=make_password(password))
            user.save()
            bridge = Bridge(userid=user, mirrorid=mirror)
            bridge.save()

            messages.success(request, 'Account created successfully')  
            return redirect('user_login')
    else:  
        form = RegistrationForm()  

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required()
def user_logout(request):
    """
        To logout to login page    
    """
    logout(request)
    messages.info(request, "Logged Out!")
    return redirect('user_login')


@login_required()
def home(request):
    """"
        To view the homepage & view all your details
    """
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


@login_required()
def save_todo(request):
    """
        To add tasks to ToDo List 
    """
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


@login_required()
def save_alarm(request):
    """
        To set the alarm
    """
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


@login_required()
def update_task_status(request):
    """
        To update the task status in the To-Do List
    """
    uid = request.user.id
    if request.method == 'POST':
        form = StatusUpdateForm(userid=uid, data=request.POST)
        if form.is_valid():
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


@login_required()
def add_mirror(request):
    """
        To add a Mirror to the DB
    """
    uid = request.user.id
    if request.method == 'POST':
        form = MirrorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['mirror_name']
            mirror = Mirror(mirror_name=name)
            mirror.save()
            messages.success(request, 'Mirror Added successfully.')
    return redirect('home')



@login_required()
def add_news_pref(request):
    """"
        To add news preferences of the user
    """
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





