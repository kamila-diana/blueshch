from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .spotify_auth import get_auth_url, exchange_code_for_token
from .spotify_metadata import find_devices
from .spotify_player import play_song
from .spotify_search import search_song

TOKEN = "TO_BE_SETUP"

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

def search(request):
    return render(request, "search.html")

@csrf_exempt
def search_api(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        query = data.get("query", "")
        token = globals().get("TOKEN", "")
        if not token or token == "TO_BE_SETUP":
            return JsonResponse({"error": "Not authenticated with Spotify."}, status=401)
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
