# Generated by Django 5.1.2 on 2024-11-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='education_system',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='grade',
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('lawyer', 'Lawyer'), ('person', 'person')], default='lawyer', max_length=20),
        ),
    ]
