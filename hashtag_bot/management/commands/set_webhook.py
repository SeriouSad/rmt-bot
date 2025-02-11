from django.core.management.base import BaseCommand
from hashtag_bot.bot.main import bot
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.delete_webhook()
        bot.set_webhook(settings.WEBHOOK_URL)
        return
