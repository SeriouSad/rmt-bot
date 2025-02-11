from django.db import models


class ChatModel(models.Model):
    tg_id = models.CharField(unique=True, verbose_name="ID беседы в телеграмм", max_length=255)
    name = models.CharField(max_length=255, verbose_name="Название беседы")
    is_superchat = models.BooleanField(default=False, verbose_name="Является суперчатом?")
    parent_chat = models.ForeignKey('self', verbose_name="Чат, в который пересылать сообщения",
                                    on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name




