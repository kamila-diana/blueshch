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


def find_devices(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
    if response.status_code == 200:
        devices = response.json().get("devices")
        print(devices)
    else:
        print("Couldn't find devices")


if __name__ == '__main__':
    access_token = "???"
    track_uri = "spotify:track:0iHZAp0Vxgvr0NjexVWkxy"
    play_song(access_token, track_uri)
