# Generated by Django 4.2.6 on 2023-11-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team_info", "0007_rename_team_team_league"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="api_id",
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]