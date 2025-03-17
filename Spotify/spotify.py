import os
from dotenv import load_dotenv
import requests
import base64
import json
import os
from Spotify.song_model import *


class Spotify:
    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

        self.access_token = os.getenv("SPOTIFY_ACCESS_TOKEN")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

    def get_currently_playing(self) -> Optional[Track]:
        request_url = "https://api.spotify.com/v1/me/player/currently-playing"
        request_headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        r = requests.get(request_url, headers=request_headers)
        if r.status_code != 200:
            return None

        response_data = r.json()

        # Extract track details
        item = response_data.get("item", {})
        if not item:
            return None

        artists = [
            Artist(
                name=artist["name"],
                id=artist["id"],
                uri=artist["uri"],
                external_url=artist["external_urls"]["spotify"]
            ) for artist in item.get("artists", [])
        ]

        album_data = item.get("album", {})
        album = Album(
            name=album_data.get("name", ""),
            id=album_data.get("id", ""),
            uri=album_data.get("uri", ""),
            external_url=album_data["external_urls"]["spotify"],
            release_date=album_data.get("release_date", ""),
            images=album_data.get("images", [])
        )

        track = Track(
            name=item.get("name", ""),
            id=item.get("id", ""),
            uri=item.get("uri", ""),
            external_url=item["external_urls"]["spotify"],
            artists=artists,
            album=album,
            duration_ms=item.get("duration_ms", 0),
            is_explicit=item.get("explicit", False),
            popularity=item.get("popularity", 0),
            progress_ms=response_data.get("progress_ms", 0),
            is_playing=response_data.get("is_playing", False)
        )

        return track

    def refresh(self):
        token_url = "https://accounts.spotify.com/api/token"
        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = requests.post(token_url, data=request_body)

        if response.status_code == 200:
            new_tokens = response.json()
            self.access_token = new_tokens.get("access_token")

            if "refresh_token" in new_tokens:
                self.refresh_token = new_tokens["refresh_token"]

            self.update_env_file()

    def update_env_file(self):
        env_path = os.path.join(os.path.dirname(__file__), "", ".env")

        with open(env_path, "r") as file:
            lines = file.readlines()

        with open(env_path, "w") as file:
            for line in lines:
                if line.startswith("SPOTIFY_ACCESS_TOKEN="):
                    file.write(f"SPOTIFY_ACCESS_TOKEN={self.access_token}\n")
                elif line.startswith("SPOTIFY_REFRESH_TOKEN=") and self.refresh_token:
                    file.write(f"SPOTIFY_REFRESH_TOKEN={self.refresh_token}\n")
                else:
                    file.write(line)




    def connect_application(self):
        auth_url = f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope=user-read-currently-playing"
        print(auth_url)

    def get_access_token(self, code):
        request_url = "https://accounts.spotify.com/api/token"

        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

        request_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {client_creds_b64}"
        }

        request_body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        r = requests.post(request_url, headers=request_headers, data=request_body)
        response_data = r.json()
        print(response_data)

        return response_data["access_token"], response_data["refresh_token"]

