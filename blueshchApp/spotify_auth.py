import base64
import secrets
import requests
from django.conf import settings
from django.urls import reverse

def generate_state():
    return secrets.token_urlsafe(16)

def get_auth_url(request):
    state = generate_state()
    request.session['spotify_auth_state'] = state
    
    params = {
        'response_type': 'code',
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'state': state,
        'scope': 'user-modify-playback-state user-read-playback-state'
    }
    
    endpoint = 'https://accounts.spotify.com/authorize'
    auth_url = f"{endpoint}?"
    auth_url += "&".join([f"{key}={value}" for key, value in params.items()])
    
    return auth_url

def exchange_code_for_token(code):
    token_url = 'https://accounts.spotify.com/api/token'
    
    credentials = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {base64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()