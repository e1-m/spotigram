import asyncio
import os

from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.types import EmojiStatus

from config import settings
from track import Track
from utils import build_listening_string, clean_whitespaces


class TelegramClientManager:
    def __init__(self):
        os.makedirs(settings.SESSIONS_PATH, exist_ok=True)
        self.tc = TelegramClient(settings.SESSIONS_PATH + 'tg_session',
                                 settings.TELEGRAM_API_ID,
                                 settings.TELEGRAM_API_HASH)
        self.default_bio: str = ''
        self.default_emoji_status: int = 0
        self.current_bio: str = ''
        self.current_emoji_status: int = 0

    async def connect(self):
        await self.tc.start()
        self.default_emoji_status = await self.get_emoji_status()
        self.default_bio = await self.get_bio() or ''
        self.current_emoji_status = self.default_emoji_status
        self.current_bio = self.default_bio

    async def get_emoji_status(self):
        me = await self.tc.get_me()
        return me.emoji_status.document_id

    async def get_bio(self):
        me = await self.tc.get_me()
        full_me = await self.tc(GetFullUserRequest(me))
        return full_me.full_user.about

    async def display_track(self, track: Track):
        self.current_emoji_status = settings.SPOTIFY_EMOJI_STATUS_ID
        self.current_bio = build_listening_string(track)
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(self.current_emoji_status)))
        await self.tc(UpdateProfileRequest(about=self.current_bio))

    async def hide_track(self):
        self.current_emoji_status = self.default_emoji_status
        self.current_bio = self.default_bio
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(self.default_emoji_status)))
        await self.tc(UpdateProfileRequest(about=self.default_bio))

    async def monitor_bio_changes(self):
        while True:
            bio = clean_whitespaces(await self.get_bio())
            if bio != clean_whitespaces(self.default_bio) and bio != clean_whitespaces(self.current_bio):
                self.default_bio = bio
            emoji_status = await self.get_emoji_status()
            if emoji_status != self.default_emoji_status and emoji_status != self.current_emoji_status:
                self.default_emoji_status = emoji_status
            await asyncio.sleep(1)
