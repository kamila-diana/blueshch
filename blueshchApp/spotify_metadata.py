import requests


def find_devices(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
    if response.status_code == 200:
        devices = response.json().get("devices")
        print("Devices: ")
        print(devices)
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return response
