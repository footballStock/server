# Generated by Django 4.2.6 on 2023-12-01 09:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_chatroom_team"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatroom",
            name="name",
        ),
    ]
