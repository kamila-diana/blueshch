import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_devices(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
    if response.status_code == 200:
        devices = response.json().get("devices")
        logger.info("Devices: ")
        logger.info(devices)
    else:
        logger.error(f"Error: {response.status_code} - {response.text}")
    return response
