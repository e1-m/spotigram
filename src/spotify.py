import asyncio
import os
from collections import defaultdict
from typing import Optional, Callable, Coroutine
from urllib.error import HTTPError
from requests.exceptions import RequestException

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors.rpcbaseerrors import RPCError
from spotipy import SpotifyOAuth, Spotify, CacheFileHandler
from spotipy.exceptions import SpotifyException

from config import settings
from track import Track


class SpotifyMonitoringException(Exception):
    pass


class SpotifyMonitor:
    def __init__(self):
        os.makedirs(settings.SESSIONS_PATH, exist_ok=True)
        self.client = Spotify(auth_manager=SpotifyOAuth(client_id=settings.SPOTIFY_CLIENT_ID,
                                                        client_secret=settings.SPOTIFY_CLIENT_SECRET,
                                                        redirect_uri=settings.REDIRECT_URL,
                                                        scope=settings.SCOPE,
                                                        cache_handler=CacheFileHandler(
                                                            cache_path=settings.SESSIONS_PATH + 'spotify.cache')
                                                        ))
        self.is_monitoring = False
        self.callbacks = defaultdict(list)

    async def start_monitoring(self):
        if self.is_monitoring:
            raise SpotifyMonitoringException('Cannot start monitoring: monitoring is already active')
        self.is_monitoring = True
        await self._monitor_playback()

    def stop_monitoring(self):
        if not self.is_monitoring:
            raise SpotifyMonitoringException('Cannot stop monitoring: monitoring is not active')
        self.is_monitoring = False

    def on_track_change(self, func: Callable[[Track], Coroutine[None, None, None]]):
        self.callbacks['on_track_change'].append(func)

    def on_playback_end(self, func: Callable[[], Coroutine[None, None, None]]):
        self.callbacks['on_playback_end'].append(func)

    def _get_current_track(self) -> Optional[Track]:
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

    async def _monitor_playback(self):
        previous_track: Optional[Track] = None
        while self.is_monitoring:
            try:
                current_track = self._get_current_track()
                if current_track:
                    if previous_track != current_track:
                        await self._fire_callbacks('on_track_change', current_track)
                        previous_track = current_track
                else:
                    if previous_track:
                        await self._fire_callbacks('on_playback_end')
                        previous_track = None
                await asyncio.sleep(settings.CHECK_TRACK_PERIOD)
            except FloodWaitError as e:
                await asyncio.sleep(settings.CHECK_TRACK_PERIOD + e.seconds)
            except (RPCError, HTTPError, RequestException):
                await self._fire_callbacks('on_playback_end')
        await self._fire_callbacks('on_playback_end')

    async def _fire_callbacks(self, event: str, *args, **kwargs):
        for callback in self.callbacks[event]:
            await callback(*args, **kwargs)
