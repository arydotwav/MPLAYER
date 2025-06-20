# Generated by Django 5.1 on 2024-08-19 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0010_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pfp',
            field=models.ImageField(default='default_pfp.jpg', upload_to='profile_pics/'),
        ),
    ]
