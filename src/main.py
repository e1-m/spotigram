import asyncio
from requests.exceptions import RequestException
from threading import Thread
from typing import Optional
from urllib.error import HTTPError

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors.rpcbaseerrors import RPCError
import pystray
from PIL import Image

from spotify import SpotifyClientManager
from telegram import TelegramClientManager
from schemas import Track
from config import settings


class TrackChangeMonitor:
    def __init__(self):
        self.telegram_client = TelegramClientManager()
        self.spotify_client = SpotifyClientManager()
        self.is_monitoring = False

    async def start_monitoring(self):
        await self.telegram_client.start()
        self.is_monitoring = True
        await self.monitor_track_change()

    def stop_monitoring(self):
        self.is_monitoring = False

    async def monitor_track_change(self):
        previous_track: Optional[Track] = None
        while self.is_monitoring:
            try:
                current_track = self.spotify_client.get_current_track()
                if current_track:
                    if previous_track != current_track:
                        await self.telegram_client.display_track(current_track)
                        previous_track = current_track
                else:
                    if previous_track:
                        await self.telegram_client.hide_track()
                        previous_track = None
                await asyncio.sleep(settings.CHECK_TRACK_PERIOD)
            except FloodWaitError as e:
                await asyncio.sleep(settings.CHECK_TRACK_PERIOD + e.seconds)
            except (RPCError, HTTPError, RequestException):
                await self.telegram_client.hide_track()
        await self.telegram_client.hide_track()


async def main():
    track_change_monitor = TrackChangeMonitor()

    icon = pystray.Icon("spotigram", Image.open("icons/icon.png"),
                        menu=pystray.Menu(pystray.MenuItem('Quit', lambda: track_change_monitor.stop_monitoring())))
    Thread(target=icon.run).start()

    await track_change_monitor.start_monitoring()

    icon.stop()


if __name__ == '__main__':
    asyncio.run(main())
