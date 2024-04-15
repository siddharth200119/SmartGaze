from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.
User = get_user_model()

def login(request):
    if request.method == 'POST':
        uid = request.POST.get('userid')
        pw = request.POST.get('password')
        user = authenticate(request, uid=uid, password=pw)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in!")
            return redirect('trial')  # Redirect to the appropriate URL after login
        else:
            print("jyfity")
            messages.warning(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')
    #     user = authenticate(uid=usrnm, password=pw)
    #     if (Mirror_Users.objects.filter(uid=usrnm, password=pw).exists()):
    #         messages.success(request, "Logged in!")
    #         login(request, user)
    #         request.session['usrnm']= usrnm
    #         # return render(request,'home.html',{'username': usrnm})
    #         return redirect('trial')
    #     else:
    #         messages.warning(request, 'Please enter valid credentials!' )
    #     return redirect('login')
    # else:
    #     return render(request, 'login.html')
    
@login_required()
def trial(request):
    return HttpResponse("HELLO")