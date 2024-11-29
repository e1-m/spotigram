import asyncio
import signal
from threading import Thread

import pystray
from PIL import Image

from spotify import SpotifyMonitor
from telegram import TelegramClientManager
from track import Track

spotify_monitor = SpotifyMonitor()
telegram_client = TelegramClientManager()


@spotify_monitor.on_track_change
async def display_track(track: Track):
    await telegram_client.display_track(track)


@spotify_monitor.on_playback_end
async def hide_track():
    await telegram_client.hide_track()


def clean_up(signum, frame):
    spotify_monitor.stop_monitoring()
    telegram_client.stop_monitoring()


signal.signal(signal.SIGINT, clean_up)
signal.signal(signal.SIGTERM, clean_up)


async def main():
    await telegram_client.connect()

    print("The app has started")
    icon = pystray.Icon("spotigram", Image.open("icons/spotigram.png"))
    icon.menu = pystray.Menu(pystray.MenuItem('Quit', lambda: (spotify_monitor.stop_monitoring() or
                                                               telegram_client.stop_monitoring() or
                                                               icon.stop())))
    Thread(target=icon.run, daemon=True).start()
    await asyncio.gather(spotify_monitor.start_monitoring(), telegram_client.start_monitoring())


if __name__ == '__main__':
    asyncio.run(main())
