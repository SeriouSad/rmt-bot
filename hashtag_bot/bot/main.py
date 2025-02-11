import telebot
import logging
from telebot import custom_filters, StateMemoryStorage
from hashtag_bot.bot.filters import DefaultChatHashtagFilter
from django.conf import settings


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(settings.BOT_TOKEN)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(DefaultChatHashtagFilter())
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


