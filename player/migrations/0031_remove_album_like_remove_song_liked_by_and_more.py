# Generated by Django 5.1 on 2024-08-31 22:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0030_remove_song_album_cover_profile_liked_albums'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='like',
        ),
        migrations.RemoveField(
            model_name='song',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_songs',
            field=models.ManyToManyField(blank=True, related_name='liked_songs', to=settings.AUTH_USER_MODEL),
        ),
    ]
