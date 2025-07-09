import requests


def play_song(access_token, track_uri):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "uris": [track_uri]
    }

    response = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        headers=headers,
        json=data
    )

    if response.status_code == 204:
        print("Success")
    else:
        print(f"Error: {response.status_code} - {response.text}")


if __name__ == '__main__':
    access_token = "YOUR_ACCESS_TOKEN"
    track_uri = "spotify:track:0iHZAp0Vxgvr0NjexVWkxy"
    play_song(access_token, track_uri)
