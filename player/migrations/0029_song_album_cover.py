# Generated by Django 5.1 on 2024-08-30 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0028_remove_album_followers_remove_artist_liked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='album_cover',
            field=models.ImageField(blank=True, null=True, upload_to='song_photo/'),
        ),
    ]
