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

    icon = pystray.Icon("spotigram", Image.open("icons/spotigram.png"),
                        menu=pystray.Menu(pystray.MenuItem('Quit', lambda: spotify_monitor.stop_monitoring())))
    Thread(target=icon.run).start()
    print("The app has started")
    asyncio.create_task(telegram_client.monitor_bio_changes())
    await spotify_monitor.start_monitoring()
    icon.stop()


if __name__ == '__main__':
    asyncio.run(main())
