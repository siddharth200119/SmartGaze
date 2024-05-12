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


        '''New Serializers'''

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mirror_Users
        fields = ['id', 'username', 'face_pattern']


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = To_do_list
        fields = ['title','due_date','task_status']

class MirrorUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mirror_Users
        fields = ['id', 'username','spotify_access_token', 'spotify_refresh_token']

class BridgeSerializer(serializers.ModelSerializer):
    user_data = MirrorUsersSerializer(source='userid', read_only=True)
    top_10_todo = serializers.SerializerMethodField()

    def get_top_10_todo(self, obj):
        top_10_todo = To_do_list.objects.filter(userid=obj.userid).order_by('due_date')[:10]
        serializer = ToDoListSerializer(top_10_todo, many=True)
        return serializer.data

    class Meta:
        model = Bridge
        fields = ['alarm_time', 'alarm_date', 'layout', 'user_data', 'top_10_todo']
