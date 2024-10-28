import asyncio

from threading import Thread
import pystray
from PIL import Image

from spotify import SpotifyMonitor
from telegram import TelegramClientManager
from schemas import Track


if __name__ == '__main__':
    spotify_monitor = SpotifyMonitor()

    telegram_client = TelegramClientManager()


    @spotify_monitor.on_track_change
    async def display_track(track: Track):
        await telegram_client.display_track(track)


    @spotify_monitor.on_playback_end
    async def hide_track():
        await telegram_client.hide_track()


    async def main():
        await telegram_client.start()

        icon = pystray.Icon("spotigram", Image.open("icons/spotigram.png"),
                            menu=pystray.Menu(pystray.MenuItem('Quit', lambda: spotify_monitor.stop_monitoring())))
        Thread(target=icon.run).start()
        print("The app has started")
        await spotify_monitor.start_monitoring()
        icon.stop()

    asyncio.run(main())
