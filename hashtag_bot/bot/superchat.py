import asyncio
from datetime import datetime, timezone, timedelta
from telethon.sync import TelegramClient
from telethon import functions, types
from django.conf import settings
from telethon.tl.types import ForumTopic, DocumentAttributeVideo, DocumentAttributeFilename


def get_chat_topics(chat_id) -> [ForumTopic]:
    # Проверяем, есть ли текущий event loop в потоке, и создаем новый, если его нет
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def fetch_topics():
        async with TelegramClient('name', settings.TG_API_ID, settings.TG_API_HASH) as client:
            result = await client(functions.channels.GetForumTopicsRequest(
                channel=int(chat_id),
                offset_date=None,
                offset_id=0,
                offset_topic=0,
                limit=100,
            ))
        topics = dict(map(lambda x: (x.title.lower(), x.id), result.topics))
        print(f"Топики полученные из teleton {topics}")
        return topics

    return loop.run_until_complete(fetch_topics())
