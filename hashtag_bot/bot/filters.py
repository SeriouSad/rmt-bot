import telebot
from hashtag_bot.models import ChatModel


class DefaultChatHashtagFilter(telebot.custom_filters.SimpleCustomFilter):
    key = 'chat_hashtags'

    @staticmethod
    def check(message, **kwargs):
        text = message.text if message.text else message.caption

        if not text or not message.chat.id < 0 or message.chat.is_forum:
            return False

        chat = ChatModel.objects.get(tg_id=message.chat.id)
        if chat.parent_chat is None:
            return False

        return True
