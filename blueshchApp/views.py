from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Token
from .spotify_auth import get_auth_url, exchange_code_for_token
from .spotify_metadata import find_devices
from .spotify_player import play_song
from .spotify_search import search_song

TOKEN = Token(user_id="user", access_token=None, expires_at=None)

def hello(request):
    return render(request, "main.html")

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

    TOKEN.update(token_info['access_token'], timezone.now())

    return HttpResponse("Authentication successful! Check your terminal for the access token.")


def play(request):
    track_uri = "spotify:track:0iHZAp0Vxgvr0NjexVWkxy"
    response = play_song(TOKEN.get_access_token(), track_uri)
    if response.status_code == 204:
        return HttpResponse("Enjoy the song!")
    else:
        return HttpResponse(f"Couldn't play the song")


def devices(request):
    response = find_devices(TOKEN.get_access_token())
    if response.status_code == 200:
        return HttpResponse("OK")
    else:
        return HttpResponse("Something is no yes.")

def search(request):
    return render(request, "search.html")

@csrf_exempt
def search_api(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        query = data.get("query", "")
        try:
            token = TOKEN.get_access_token()
        except ValueError as e:
            print(f"Error getting access token: {e}")
            return JsonResponse({"error": "Error getting access token"}, status=401)
        if len(query) > 100:
            return JsonResponse({"error": "Query too long."}, status=400)
        if not query:
            return JsonResponse({"results": []})
        results = search_song(query, token)
        tracks = results.get("tracks", {}).get("items", [])
        table = [
            {
                "name": t["name"],
                "artist": ", ".join(a["name"] for a in t["artists"]),
                "album": t["album"]["name"],
                "uri": t["uri"]
            }
            for t in tracks
        ]
        return JsonResponse({"results": table})
    return JsonResponse({"error": "Invalid request."}, status=400)
