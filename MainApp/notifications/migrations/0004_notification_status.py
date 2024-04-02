# Generated by Django 5.0.3 on 2024-04-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_remove_notification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('Read', 'Read'), ('Not Read', 'Not Read')], default='Not Read', max_length=10),
        ),
    ]