from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.types import EmojiStatus

from config import settings


class TelegramClientManager:
    def __init__(self):
        self.tc = TelegramClient('tg_session', settings.API_ID, settings.API_HASH)

    async def start(self):
        await self.tc.start(phone=settings.PHONE, password=settings.PASSWORD)

    async def get_current_emoji_status(self) -> int:
        me = await self.tc.get_me()
        return me.emoji_status.document_id

    async def get_current_bio(self) -> str:
        me = await self.tc.get_me()
        full_me = await self.tc(GetFullUserRequest(me))
        return full_me.full_user.about

    async def update_bio(self, about: str) -> None:
        await self.tc(UpdateProfileRequest(about=about))

    async def update_emoji_status(self, document_id: int) -> None:
        await self.tc(UpdateEmojiStatusRequest(EmojiStatus(document_id)))
