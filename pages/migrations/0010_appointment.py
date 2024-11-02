# Generated by Django 5.1.1 on 2024-10-01 20:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_contactmessage_created_at_faq_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]