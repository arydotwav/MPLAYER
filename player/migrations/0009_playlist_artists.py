# Generated by Django 5.1 on 2024-08-17 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_song_songcover'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='artists',
            field=models.ManyToManyField(related_name='playlists', to='player.artist'),
        ),
    ]
