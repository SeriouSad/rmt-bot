from datetime import datetime, timedelta
from typing import List
import asyncio

from django.conf import settings

from config.celery import app
from telebot import types
from telethon.sync import TelegramClient

from hashtag_bot.bot.main import bot
from hashtag_bot.bot.superchat import get_chat_topics
from hashtag_bot.models import ChatModel


@app.task
def process_message(message_id, chat_id, message_date, hashtags: List[str], text, media_group_id=None, reply_message_id=None):
    chat = ChatModel.objects.get(tg_id=chat_id)
    topics = get_chat_topics(chat.parent_chat.tg_id)
    print(topics)
    unrecognized_topics = []

    for i in hashtags:
        if i not in topics.keys():
            unrecognized_topics.append(i)
        else:
            message_thread_id = topics[i]
            if media_group_id:
                asyncio.run(fetch_and_forward_messages(chat.tg_id, media_group_id,
                                                datetime.fromtimestamp(message_date) - timedelta(minutes=1),
                                               chat.parent_chat.tg_id, message_thread_id, text))

            else:
                if reply_message_id:
                    id_list = [reply_message_id, message_id]
                else:
                    id_list = [message_id]
                bot.forward_messages(
                chat_id=chat.parent_chat.tg_id,
                from_chat_id=chat.tg_id,
                message_ids=id_list,
                message_thread_id=message_thread_id,
                )

    if unrecognized_topics:
        text = "Не обработаны следующие хештеги:\n"
        for hashtag in unrecognized_topics:
            text += f"{hashtag}\n"
        text += "\nИсправьте их и отправьте сообщение снова"
        bot.send_message(chat_id, text, reply_to_message_id=message_id)


async def fetch_and_forward_messages(chat_id, media_group_id, message_time: datetime, target_chat_id, thread_id, text):
    async with TelegramClient('name', settings.TG_API_ID, settings.TG_API_HASH) as client:
        messages = await client.get_messages(int(chat_id), offset_date=message_time, reverse=True, limit=100)
        album_messages = [msg for msg in messages if msg.grouped_id == int(media_group_id)]
        if album_messages:
            await client.send_message(
                entity=int(target_chat_id),  # Чат, куда пересылаем сообщение
                file=album_messages,  # ID сообщения, которое пересылаем  # Откуда пересылаем сообщение
                reply_to=thread_id,
                message=text
            )
