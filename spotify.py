from spotipy import SpotifyOAuth, Spotify

from config import settings


class SpotifyClient:
    def __init__(self):
        self.client = Spotify(auth_manager=SpotifyOAuth(client_id=settings.SPOTIFY_CLIENT_ID,
                                                        client_secret=settings.SPOTIFY_CLIENT_SECRET,
                                                        redirect_uri=settings.REDIRECT_URL,
                                                        scope=settings.SCOPE))

    def get_current_track(self) -> str | None:
        current_playback = self.client.current_playback()

        if current_playback and current_playback['is_playing']:
            current_track = current_playback['item']
            track_name = current_track['name']
            artists = ', '.join([artist['name'] for artist in current_track['artists']])
            return f"Currently listening to: {track_name} by {artists}"
        else:
            return None
