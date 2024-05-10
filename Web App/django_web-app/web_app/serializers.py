from .models import *
from rest_framework import serializers



class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = To_do_list
        fields = ['title','due_date','task_status','userid']


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bridge
        fields = ['userid','alarm_date','alarm_time']


class UserSerializer(serializers.ModelSerializer):
    todo = ToDoSerializer(many=True, read_only=True)
    class Meta:
        model = Mirror_Users
        fields = ['id','face_pattern','todo']