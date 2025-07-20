import requests

def search_song(query, token):
    endpoint = "https://api.spotify.com/v1/search"
    params={"q": query, "type": "track"}
    headers={"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, params=params, headers=headers)
    return response.json()
