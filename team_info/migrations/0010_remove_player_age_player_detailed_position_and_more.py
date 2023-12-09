# Generated by Django 4.2.6 on 2023-11-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team_info", "0009_remove_player_detailed_position_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="player",
            name="age",
        ),
        migrations.AddField(
            model_name="player",
            name="detailed_position",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="player",
            name="nationality",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
