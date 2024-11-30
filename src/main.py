import asyncio
import signal
from threading import Thread, Lock

import pystray
from PIL import Image

from spotify import SpotifyMonitor, SpotifyMonitoringException
from telegram import TelegramClientManager, TelegramMonitoringException
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
    try_stop_monitoring()


def try_stop_monitoring():
    try:
        spotify_monitor.stop_monitoring()
        telegram_client.stop_monitoring()
    except (SpotifyMonitoringException, TelegramMonitoringException):
        pass


signal.signal(signal.SIGINT, clean_up)
signal.signal(signal.SIGTERM, clean_up)


async def main():
    await telegram_client.connect()

    print("The app has started")
    paused = Lock()

    def pause():
        nonlocal paused
        paused.acquire(blocking=True)
        try_stop_monitoring()

    while True:
        icon = pystray.Icon("spotigram", Image.open("icons/spotigram.png"))
        icon.menu = pystray.Menu(pystray.MenuItem('Quit', lambda icn: try_stop_monitoring() or icn.stop()),
                                 pystray.MenuItem('Resume', lambda icn: paused.release() or icn.stop())
                                 if paused.locked() else
                                 pystray.MenuItem('Pause', lambda icn: pause() or icn.stop()))
        Thread(target=icon.run, daemon=True).start()
        if paused.locked():
            paused.acquire(blocking=True)
            paused.release()
            continue
        await asyncio.gather(spotify_monitor.start_monitoring(), telegram_client.start_monitoring())
        # if monitoring is finished, but not paused, exit
        if not paused.locked():
            break


if __name__ == '__main__':
    asyncio.run(main())
