# Generated by Django 5.1 on 2024-08-17 06:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_song_audio_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_songs', to=settings.AUTH_USER_MODEL),
        ),
    ]
