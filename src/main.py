import asyncio

from spotify import SpotifyClientManager
from telegram import TelegramClientManager
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.types import EmojiStatus

from config import settings


async def main():
    telegram_client = TelegramClientManager()
    await telegram_client.start()
    spotify_client = SpotifyClientManager()

    previous_track: str = ""
    settings.DEFAULT_EMOJI_STATUS_ID = await telegram_client.get_current_emoji_status()
    settings.DEFAULT_BIO = await telegram_client.get_current_bio()

    while True:
        try:
            current_track = spotify_client.get_current_track()
            if not current_track:
                if previous_track:
                    await telegram_client.update_bio(settings.DEFAULT_BIO)
                    await telegram_client.update_emoji_status(settings.DEFAULT_EMOJI_STATUS_ID)
                    previous_track = ""
                continue
            if previous_track != current_track:
                await telegram_client.update_bio(current_track)
                await telegram_client.update_emoji_status(settings.SPOTIFY_EMOJI_STATUS_ID)
                previous_track = current_track
            await asyncio.sleep(1)
        except Exception:
            await telegram_client.update_bio(settings.DEFAULT_BIO)
            await telegram_client.update_emoji_status(settings.DEFAULT_EMOJI_STATUS_ID)


if __name__ == '__main__':
    asyncio.run(main())
