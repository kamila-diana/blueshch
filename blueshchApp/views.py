from django.shortcuts import redirect
from django.http import HttpResponse
from .spotify_auth import get_auth_url, exchange_code_for_token
from .spotify_metadata import find_devices
from .spotify_player import play_song

TOKEN = "TO_BE_SETUP"


def login(request):
    auth_url = get_auth_url(request)
    return redirect(auth_url)

def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('spotify_auth_state')
    
    if state is None or state != stored_state:
        return HttpResponse("State mismatch. Authorization failed.", status=400)
    
    token_info = exchange_code_for_token(code)
    
    if 'error' in token_info:
        return HttpResponse(f"Error: {token_info['error']}", status=400)
    
    # Print token in terminal for demonstration
    print("\nSpotify Access Token:", token_info['access_token'])

    global TOKEN
    TOKEN = token_info['access_token']

    return HttpResponse("Authentication successful! Check your terminal for the access token.")


def play(request):
    track_uri = "spotify:track:0iHZAp0Vxgvr0NjexVWkxy"
    response = play_song(TOKEN, track_uri)
    if response.status_code == 204:
        return HttpResponse("Enjoy the song!")
    else:
        return HttpResponse(f"Couldn't play the song")


def devices(request):
    response = find_devices(TOKEN)
    if response.status_code == 200:
        return HttpResponse("OK")
    else:
        return HttpResponse("Something is no yes.")
