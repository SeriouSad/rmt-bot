from django.db import IntegrityError
from telebot import types
from hashtag_bot.bot.main import bot
from hashtag_bot.bot.texts import WELCOME_MESSAGE
from hashtag_bot.models import ChatModel
from hashtag_bot.tasks import process_message
import re


def process_media_message(message: types.Message):
    print(message)
    text = message.text if message.text else message.caption
    hashtags = re.findall(r'#\w+', text)
    hashtags = list(map(lambda x: x.lower(), hashtags))
    print(text)
    if message.reply_to_message:
        reply_text = message.reply_to_message.text if message.reply_to_message.text else message.reply_to_message.caption
        if reply_text:
            text += f"\n\nТекст искомого сообщения:\n{reply_text}"
        process_message.delay(message.message_id, message.chat.id, message.reply_to_message.date, hashtags, text, message.reply_to_message.media_group_id, message.reply_to_message.message_id)
    else:
        process_message.delay(message.id, message.chat.id, message.date, hashtags, text, message.media_group_id)


@bot.message_handler(content_types=['new_chat_members'])
def send_welcome(message: types.Message):
    bot_id = bot.get_me().id
    try:
        ChatModel.objects.create(tg_id=message.chat.id, name=message.chat.title, is_superchat=bool(message.chat.is_forum))
    except IntegrityError:
        pass
    for chat_member in message.new_chat_members:
        if chat_member.id == bot_id:
            bot.send_message(message.chat.id, WELCOME_MESSAGE)


@bot.message_handler(chat_hashtags=True, content_types=['text', 'photo', 'document', 'video'])
def handle_message(message: types.Message):
    process_media_message(message)
    print(f"Сообщение новое {message}")


@bot.edited_message_handler(chat_hashtags=True, content_types=['text', 'photo', 'document', 'video'])
def handle_edit(message: types.Message):
    process_media_message(message)
    print(f"Сообщение изменено {message}")




