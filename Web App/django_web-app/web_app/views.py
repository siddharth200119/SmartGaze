from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
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


@login_required()
def update_task_status(request):
    uid = request.user.id
    try:
        task = To_do_list.objects.get(tid=3)
        if request.method == 'POST':
            form = StatusUpdateForm(request.POST, userid=uid)
            print("DONE")
            if form.is_valid():
                tid = form.cleaned_data['tid']
                status = form.cleaned_data['status']
                updated_task = To_do_list.objects.filter(tid=tid).update(task_status=status)
                
                messages.success(request, 'Task status updated successfully.')
                return redirect('home')
        # else:
            # form = TodoListUpdateForm(instance=task)
        # return render(request, 'update_task_status.html', {'form': form, 'task': task})
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


# class Todosapi(api_view):
#         def get(self, request):
#             uid = request.user
#             data = To_do_list.objects.filter(userid=uid)
#             serializer = ToDoSerializer(data, many=True)
#             print(data)
#             return Response({
#                 'message': 'Added data',
#                 'data': serializer.data
#                 })


#API to get the details of the Alarm
@api_view(["GET"])
def alarm_api(request, userid):
    uid = request.user
    data = Bridge.objects.filter(userid=userid)
    serializer = AlarmSerializer(data, many=True)
    return Response({
        'data': serializer.data
        })


#API to get the details of the User's face pattern with user ID
@api_view(["GET"])
def user_api(request, userid):
    data = User.objects.filter(userid=userid)
    serializer = UserSerializer(data, many=True)
    return Response({
        'data': serializer.data
        })