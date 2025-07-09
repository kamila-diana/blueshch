from django.shortcuts import redirect
from django.http import HttpResponse
from .spotify_auth import get_auth_url, exchange_code_for_token

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
    
    return HttpResponse("Authentication successful! Check your terminal for the access token.")
