"""
    Serializers for The SmartGaze Web App
"""
from .models import *
from rest_framework import serializers


class AlarmSerializer(serializers.ModelSerializer):
    """
        Serializer to get Alarm details format
    """
    class Meta:
        model = Bridge
        fields = ['userid','alarm_date','alarm_time']


class SpotifySerializer(serializers.ModelSerializer):
    """
        Serializer to get Spotify tokens 
    """
    class Meta:
        model = Mirror_Users
        fields = ['id','spotify_access_token', 'spotify_refresh_token']


class UsersSerializer(serializers.ModelSerializer):
    """
        Serializer to get User's face pattern  
    """
    class Meta:
        model = Mirror_Users
        fields = ['id', 'username', 'face_pattern']


class ToDoListSerializer(serializers.ModelSerializer):
    """
        Serializer to get User's ToDo List tasks
    """
    class Meta:
        model = To_do_list
        fields = ['title','due_date','task_status']


class MirrorUsersSerializer(serializers.ModelSerializer):
    """
        Serializer to get Spotify tokens
    """
    class Meta:
        model = Mirror_Users
        fields = ['id', 'username', 'spotify_access_token']

class NewsSerializer(serializers.ModelSerializer):
    """
        Serializer to get User's Preferred News Topics
    """
    class Meta:
        model = News_pref
        fields = ['topic']


class BridgeSerializer(serializers.ModelSerializer):
    """
        Serializer to get the data necessary for the home screen of the Smart Mirror
    """
    user_data = MirrorUsersSerializer(source='userid', read_only=True)
    topics = serializers.SerializerMethodField()
    top_10_todo = serializers.SerializerMethodField()

    def get_top_10_todo(self, obj):
        top_10_todo = To_do_list.objects.filter(userid=obj.userid).order_by('due_date')[:10]
        serializer = ToDoListSerializer(top_10_todo, many=True)
        return serializer.data

    def get_topics(self, obj):
        news_prefs = News_pref.objects.filter(userid=obj.userid)
        topics_list = [" OR ".join(news_pref.topic.split(',')) for news_pref in news_prefs]
        topics_string = " OR ".join(topics_list)
        return topics_string

    class Meta:
        model = Bridge
        fields = ['alarm_time', 'alarm_date', 'layout', 'user_data', 'top_10_todo','topics']
