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
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'item_description': 'Task Description',
        }
        

#Form to set the alarm
class AlarmForm(forms.ModelForm):
    class Meta:
        model = Bridge
        fields = ['mirrorid', 'alarm_date','alarm_time']
        widgets = {
            'alarm_time': forms.TimeInput(attrs={'type': 'time', 'format': '%I:%M %p'}),
            'alarm_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
#Form to update the status of a particular Task
class StatusUpdateForm(forms.ModelForm):
    task_status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    tid = forms.ModelChoiceField(queryset=None, label='Task ID') 

    def __init__(self, userid, *args, **kwargs):
        super(StatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tid'].queryset = To_do_list.objects.filter(userid=userid)

    class Meta:
        model = To_do_list
        fields = ['tid','task_status']


#Form to add a Mirror to the DB
class MirrorForm(forms.ModelForm):
    class Meta:
        model = Mirror
        fields = ['mirror_name']
        labels = {
            'mirror_name': 'Mirror Name'
        }
        

#Form to add a Mirror to the DB
class NewsForm(forms.ModelForm):
    class Meta:
        model = News_pref
        fields = ['topic']
        labels = {
            'topic': 'Topic for News Headlines'
        }
        

