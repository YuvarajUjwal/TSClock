# Generated by Django 5.0.2 on 2024-02-16 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tango', '0006_video_video_up'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_up',
        ),
    ]
