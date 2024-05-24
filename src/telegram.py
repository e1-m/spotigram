from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.types import EmojiStatus

from config import settings
from schemas import Track
from utils import get_listening_to_track_string


class TelegramClientManager:
    def __init__(self):
        self.tc = TelegramClient('tg_session', settings.API_ID, settings.API_HASH)

    async def start(self):
        await self.tc.start(phone=settings.PHONE, password=settings.PASSWORD)
        me = await self.tc.get_me()
        full_me = await self.tc(GetFullUserRequest(me))
        settings.DEFAULT_EMOJI_STATUS_ID = me.emoji_status.document_id
        settings.DEFAULT_BIO = full_me.full_user.about

    async def display_track(self, track: Track):
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(settings.SPOTIFY_EMOJI_STATUS_ID)))
        await self.tc(UpdateProfileRequest(about=get_listening_to_track_string(track)))

    async def hide_track(self):
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(settings.DEFAULT_EMOJI_STATUS_ID)))
        await self.tc(UpdateProfileRequest(about=settings.DEFAULT_BIO))
