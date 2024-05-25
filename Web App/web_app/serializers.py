from .models import *
from rest_framework import serializers

# class ToDoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = To_do_list
#         fields = ['title','due_date','task_status','userid']


# Serializer to send Alarm details in json format
class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bridge
        fields = ['userid','alarm_date','alarm_time']


        '''New Serializers'''


# Serializer to send Spotify tokens in JSON
class SpotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mirror_Users
        fields = ['id','spotify_access_token', 'spotify_refresh_token']


# Serializer to send User's face pattern  in JSON
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mirror_Users
        fields = ['id', 'username', 'face_pattern']


# Serializer to send User's ToDo List tasks in JSON
class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = To_do_list
        fields = ['title','due_date','task_status']


# Serializer to send Spotify tokens in JSON
class MirrorUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mirror_Users
        fields = ['id', 'username', 'spotify_access_token']

# Serializer to send Spotify tokens in JSON
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News_pref
        fields = ['topic']


class BridgeSerializer(serializers.ModelSerializer):
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
