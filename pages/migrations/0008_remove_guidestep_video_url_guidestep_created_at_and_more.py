# Generated by Django 5.1.1 on 2024-10-01 19:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_guidestep'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guidestep',
            name='video_url',
        ),
        migrations.AddField(
            model_name='guidestep',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='guidestep',
            name='video',
            field=models.FileField(default='videos/default.mp4', upload_to='videos/guide'),
        ),
    ]