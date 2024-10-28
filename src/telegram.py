import os

from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.types import EmojiStatus

from config import settings
from schemas import Track
from utils import build_listening_to_string


class TelegramClientManager:
    def __init__(self):
        os.makedirs(settings.SESSIONS_PATH, exist_ok=True)
        self.tc = TelegramClient(settings.SESSIONS_PATH + 'tg_session',
                                 settings.TELEGRAM_API_ID,
                                 settings.TELEGRAM_API_HASH)
        self.default_bio: str = ''
        self.default_emoji_status_id: int = 0

    async def start(self):
        await self.tc.start(phone=settings.PHONE, password=settings.PASSWORD)
        me = await self.tc.get_me()
        full_me = await self.tc(GetFullUserRequest(me))
        self.default_emoji_status_id = me.emoji_status.document_id
        self.default_bio = full_me.full_user.about or ''

    async def display_track(self, track: Track):
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(settings.SPOTIFY_EMOJI_STATUS_ID)))
        await self.tc(UpdateProfileRequest(about=build_listening_to_string(track)))

    async def hide_track(self):
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(self.default_emoji_status_id)))
        await self.tc(UpdateProfileRequest(about=self.default_bio))
