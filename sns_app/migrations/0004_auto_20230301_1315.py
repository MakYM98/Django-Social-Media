# Generated by Django 3.2 on 2023-03-01 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns_app', '0003_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='sender',
        ),
        migrations.AddField(
            model_name='messages',
            name='chat',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
