from typing import Optional

from spotipy import SpotifyOAuth, Spotify
from spotipy.exceptions import SpotifyException

from config import settings
from schemas import Track


class SpotifyClientManager:
    def __init__(self):
        self.client = Spotify(auth_manager=SpotifyOAuth(client_id=settings.SPOTIFY_CLIENT_ID,
                                                        client_secret=settings.SPOTIFY_CLIENT_SECRET,
                                                        redirect_uri=settings.REDIRECT_URL,
                                                        scope=settings.SCOPE))

    def get_current_track(self) -> Optional[Track]:
        try:
            playback = self.client.current_playback()
            if playback and playback.get('is_playing'):
                if track := playback.get('item'):
                    name = track['name']
                    artists = ', '.join([artist['name'] for artist in track['artists']])
                    link = track['external_urls']['spotify']
                    return Track(name=name, artists=artists, link=link)
        except SpotifyException:
            return None
