import asyncio
from typing import Optional

from spotify import SpotifyClientManager
from telegram import TelegramClientManager
from telethon.errors.rpcerrorlist import FloodWaitError

from config import settings
from src.schemas import Track
from utils import get_listening_to_track_string


async def main():
    telegram_client = TelegramClientManager()
    await telegram_client.start()
    spotify_client = SpotifyClientManager()

    previous_track: Optional[Track] = None
    while True:
        try:
            current_track = spotify_client.get_current_track()
            if not current_track:
                if previous_track:
                    await telegram_client.hide_track()
                    previous_track = None
                continue

            if previous_track != current_track:
                await telegram_client.display_track(current_track)
                previous_track = current_track
            await asyncio.sleep(1)
        except FloodWaitError as e:
            await asyncio.sleep(5+e.seconds)
        except Exception:
            await telegram_client.hide_track()


if __name__ == '__main__':
    asyncio.run(main())
