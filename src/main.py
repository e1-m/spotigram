import asyncio
from threading import Thread

import pystray
from PIL import Image

from spotify import SpotifyMonitor
from telegram import TelegramClientManager
from track import Track


async def main():
    spotify_monitor = SpotifyMonitor()
    telegram_client = TelegramClientManager()
    await telegram_client.connect()

    @spotify_monitor.on_track_change
    async def display_track(track: Track):
        await telegram_client.display_track(track)

    @spotify_monitor.on_playback_end
    async def hide_track():
        await telegram_client.hide_track()

    print("The app has started")
    icon = pystray.Icon("spotigram", Image.open("icons/spotigram.png"))
    icon.menu = pystray.Menu(pystray.MenuItem('Quit', lambda: spotify_monitor.stop_monitoring() or icon.stop()))
    Thread(target=icon.run).start()
    await asyncio.wait(
        [asyncio.create_task(spotify_monitor.start_monitoring()),
         asyncio.create_task(telegram_client.monitor_bio_changes())],
        return_when=asyncio.FIRST_COMPLETED
    )


if __name__ == '__main__':
    asyncio.run(main())
