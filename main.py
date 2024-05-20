from time import sleep

from spotify import SpotifyClient
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

from config import settings


telegram_client = TelegramClient('tg_session', settings.API_ID, settings.API_HASH)
telegram_client.start(phone=settings.PHONE, password=settings.PASSWORD)


async def update_status(status: str):
    await telegram_client(UpdateProfileRequest(about=status))


async def main():
    spotify_client = SpotifyClient()
    while True:
        current_track = spotify_client.get_current_track()
        if not current_track:
            continue
        await update_status(current_track)
        sleep(5)


if __name__ == '__main__':
    telegram_client.loop.run_until_complete(main())
