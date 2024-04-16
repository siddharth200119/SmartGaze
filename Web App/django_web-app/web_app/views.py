from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *
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
            # return render(request, 'home.html') 
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


#Function to view the homepage with all the tasks & set the alarm
@login_required()
def home(request):
    tasks = None
    if request.method == 'POST':
        todoform = TodoListForm(request.POST)
        alarmform = AlarmForm(request.POST)
        if todoform.is_valid():  
            title = todoform.cleaned_data['title']
            itemd = todoform.cleaned_data['item_description']
            date = todoform.cleaned_data['due_date']

            alarm_time = alarmform.cleaned_data['atime']
            alarm_date = alarmform.cleaned_data['adate']
            uid = request.user
            task = To_do_list(title=title, item_description=itemd, due_date=date, userid=uid)
            task.save()
            alarm = Alarm(userid=uid, alarm_date=alarm_date, alarm_time=alarm_time)
            alarm.save()
    else:
        todoform = TodoListForm()
        alarmform = AlarmForm()
        uid = request.user
        try:
            tasks = To_do_list.objects.filter(userid=uid)
        except To_do_list.DoesNotExist:
            pass
    context = {'todoform': todoform,
                'alarmform': alarmform,
                'tasks': tasks}
    return render(request, 'home.html', context)