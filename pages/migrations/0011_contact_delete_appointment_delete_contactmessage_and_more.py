# Generated by Django 5.1.3 on 2024-11-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.DeleteModel(
            name='ContactMessage',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='category',
        ),
        migrations.DeleteModel(
            name='GuideStep',
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.DeleteModel(
            name='Testimonial',
        ),
        migrations.DeleteModel(
            name='FAQ',
        ),
        migrations.DeleteModel(
            name='FAQCategory',
        ),
    ]
