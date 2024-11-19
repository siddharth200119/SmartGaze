"""
    APIs for The SmartGaze Web App to interact with the SmartGaze Mirror 
"""

from django.shortcuts import redirect, HttpResponse, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework import status
import base64
import json
import requests
from urllib.parse import urlencode
from .models import *
from .serializers import *
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv, find_dotenv
import os
dotenv_path = find_dotenv('../.env')
load_dotenv(dotenv_path)

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

User = get_user_model()


@api_view(["GET"])
def alarm_api(request, mirrorid):
    """"
        API - To GET the details of the pre-set Alarm of specific Mirror
    """
    uid = request.user
    data = Bridge.objects.filter(mirrorid=mirrorid).order_by('alarm_date', 'alarm_time')
    serializer = AlarmSerializer(data, many=True)
    return Response({
        'data': serializer.data
        })


@api_view(["GET"])
def get_face_patterns_api(request, mirrorid):
    """"
        API - To GET the details of the User's face pattern with user ID & username
    """
    bridge_data = Bridge.objects.filter(mirrorid=mirrorid)
    serialized_data = []

    for bridge_obj in bridge_data:
        user_serializer = UsersSerializer(bridge_obj.userid)
        serialized_data.append({
            'userid': bridge_obj.userid.id,
            'username': user_serializer.data['username'],
            'face_pattern': user_serializer.data['face_pattern']
        })

    return Response({'data': serialized_data})



@api_view(["GET"])
def get_everything_api(request, userid):
    """"
        API - To GET all the user's data & refresh the Spotify access token 
    """
    bridge_data = Bridge.objects.filter(userid=userid).first()
    if not bridge_data:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = get_object_or_404(Mirror_Users, id=userid)
    refresh_token = user.spotify_refresh_token
    uid=request.user.id
    # print(refresh_token)

    client_id = spotify_client_id
    client_secret = spotify_client_secret

    credentials = f"{client_id}:{client_secret}"

    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Basic {encoded_credentials}"
        },
        'data': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    }

    response = requests.post(auth_options['url'], headers=auth_options['headers'], data=auth_options['data'])
    # print(response)

    if response.status_code == 200:
        body = response.json()
        access_token = body.get('access_token')
        new_refresh_token = body.get('refresh_token', refresh_token)  
        
        Mirror_Users.objects.filter(id=uid).update(spotify_access_token=access_token)
        Mirror_Users.objects.filter(id=uid).update(spotify_refresh_token=new_refresh_token)
    else:
        return HttpResponse("ERROR RESPONSE FROM SPOTIFY")

    serializer = BridgeSerializer(bridge_data)

    return Response(serializer.data)


@api_view(["GET"])
def get_token_api(request, userid):
    """
        API - To GET all the user's spotify access token & refresh token
    """
    user_data = Mirror_Users.objects.filter(id=userid).first()
    if not user_data:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)

    serializer = SpotifySerializer(user_data)
    return Response(serializer.data)


@api_view(["GET"])
def spotify_login(request):
    """
    Allowed Method: GET

        API - To Login to spotify using spotify SDK Endpoints
    """
    scope = "streaming \
               user-read-email \
               user-read-private"
    auth_query_parameters = {
        "response_type": "code",
        "client_id": spotify_client_id,
        "scope": scope,
        "redirect_uri": "http://localhost:8000/spotify/callback"
    }
    authorization_url = 'https://accounts.spotify.com/authorize/?' + urlencode(auth_query_parameters)
    return redirect(authorization_url)


@login_required()
@api_view(["GET"])
def spotify_callback(request):
    """
        API - To GET the access & refresh token by passing the code to the Spotify API Endpoint
    """
    code = request.GET.get('code')
    if code:
        token_url = 'https://accounts.spotify.com/api/token'

        redirect_uri = 'http://localhost:8000/spotify/callback'

        form_data = {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        auth_header = base64.b64encode(f'{spotify_client_id}:{spotify_client_secret}'.encode()).decode('utf-8')

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded',
            "Access-Control-Allow-Credentials": "true"
        }

        response = requests.post(token_url, data=form_data, headers=headers)

        content = json.loads(response.content)
        access_token=content['access_token']
        refresh_token = content['refresh_token']
        uid = request.user.id
        # print("after spotify", uid)
        Mirror_Users.objects.filter(id=uid).update(spotify_access_token=access_token)
        Mirror_Users.objects.filter(id=uid).update(spotify_refresh_token=refresh_token)

        if response.status_code == 200:
            access_token = response.json()['access_token']
            return redirect('home')
        else:
            return redirect('/error')

    else:
        return redirect('/error')



