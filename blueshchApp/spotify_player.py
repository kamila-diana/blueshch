import requests
import logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    if response.status_code == 204:
        logging.info("Success")
    else:
        logging.error(f"Error: {response.status_code} - {response.text}")
        logger.info("Success")
    else:
        logger.error(f"Error: {response.status_code} - {response.text}")

    return response
