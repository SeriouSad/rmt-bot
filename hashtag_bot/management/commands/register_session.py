import asyncio

from django.core.management.base import BaseCommand
from telethon.sync import TelegramClient
from django.conf import settings


class Command(BaseCommand):
    @staticmethod
    async def connect():
        async with TelegramClient("name", settings.TG_API_ID, settings.TG_API_HASH) as client:
            print(await client.get_me())
        return

    def handle(self, *args, **options):
        asyncio.run(self.connect())
