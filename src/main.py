import asyncio
from typing import Optional

from spotify import SpotifyClientManager
from telegram import TelegramClientManager
from telethon.errors.rpcerrorlist import FloodWaitError, AboutTooLongError

from src.schemas import Track


async def main():
    telegram_client = TelegramClientManager()
    spotify_client = SpotifyClientManager()

    await telegram_client.start()

    previous_track: Optional[Track] = None
    while True:
        try:
            current_track = spotify_client.get_current_track()
            if current_track:
                if previous_track != current_track:
                    await telegram_client.display_track(current_track)
                    previous_track = current_track
            else:
                if previous_track:
                    await telegram_client.hide_track()
                    previous_track = None
            await asyncio.sleep(1)
        except FloodWaitError as e:
            await asyncio.sleep(5 + e.seconds)
        except AboutTooLongError:
            await telegram_client.hide_track()


if __name__ == '__main__':
    asyncio.run(main())
