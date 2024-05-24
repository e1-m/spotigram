from typing import Optional

from spotipy import SpotifyOAuth, Spotify

from config import settings
from schemas import Track


class SpotifyClientManager:
    def __init__(self):
        self.client = Spotify(auth_manager=SpotifyOAuth(client_id=settings.SPOTIFY_CLIENT_ID,
                                                        client_secret=settings.SPOTIFY_CLIENT_SECRET,
                                                        redirect_uri=settings.REDIRECT_URL,
                                                        scope=settings.SCOPE))

    def get_current_track(self) -> Optional[Track]:
        current_playback = self.client.current_playback()

        if current_playback and current_playback['is_playing']:
            current_track = current_playback['item']

            name = current_track['name']
            artists = ', '.join([artist['name'] for artist in current_track['artists']])
            link = current_track['external_urls']['spotify']

            return Track(name=name, artists=artists, link=link)
