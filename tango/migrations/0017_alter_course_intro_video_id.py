# Generated by Django 5.0.2 on 2024-03-11 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tango', '0016_course_course_details_course_intro_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='Intro_Video_ID',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
