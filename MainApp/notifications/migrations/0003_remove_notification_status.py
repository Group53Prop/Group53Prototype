# Generated by Django 5.0.3 on 2024-04-02 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='status',
        ),
    ]