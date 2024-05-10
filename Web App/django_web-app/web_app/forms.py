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
        

#Form to set the alarm
class AlarmForm(forms.ModelForm):
    class Meta:
        model = Bridge
        fields = ['mirrorid', 'alarm_date','alarm_time']
        widgets = {
            'alarm_time': forms.TimeInput(attrs={'type': 'time', 'format': '%I:%M %p'}),
            'alarm_date': forms.DateInput(attrs={'type': 'date'}),
        }
        


class StatusUpdateForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    tid = forms.ModelChoiceField(queryset=None, label='Task') 

    def __init__(self, userid, *args, **kwargs):
        super(StatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tid'].queryset = To_do_list.objects.filter(userid=userid)
    class Meta:
        model = To_do_list
        fields = ['tid','status']




