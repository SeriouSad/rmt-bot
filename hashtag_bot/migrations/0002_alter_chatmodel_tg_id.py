# Generated by Django 5.1.5 on 2025-02-05 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtag_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmodel',
            name='tg_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='ID беседы в телеграмм'),
        ),
    ]
