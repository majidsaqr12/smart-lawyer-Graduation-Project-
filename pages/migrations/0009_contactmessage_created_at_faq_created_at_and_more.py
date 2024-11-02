# Generated by Django 5.1.1 on 2024-10-01 19:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_remove_guidestep_video_url_guidestep_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='faq',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]