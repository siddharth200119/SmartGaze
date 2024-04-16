from django import forms
from .models import *

#Form to register a new account
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-Enter your password'}))
    class Meta:
        model = Mirror_Users
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'E.g., John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'E.g., Doe'}),
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        }


#Form to add a task to ToDo
class TodoListForm(forms.ModelForm):
    class Meta:
        model = To_do_list
        fields = ['title','item_description','due_date']
        widgets = {
            'title': forms.TextInput(),
            'item_description': forms.TextInput(),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        required = {
            'title': False,
            'item_description': False,
            'due_date': False,
        }

#Form to set the alarm
class AlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = ['alarm_date','alarm_time']
        widgets = {
            'alarm_time': forms.TimeInput(attrs={'type': 'time'}),
            'alarm_date': forms.DateInput(attrs={'type': 'date'}),
        }
        required = {
            'alarm_time': False,
            'alarm_date': False,
        }