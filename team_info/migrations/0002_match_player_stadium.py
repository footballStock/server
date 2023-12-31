# Generated by Django 4.2.6 on 2023-11-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team_info", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("result", models.CharField(max_length=255)),
                ("opponent", models.CharField(max_length=255)),
                (
                    "match_type",
                    models.CharField(
                        choices=[("league", "리그 경기"), ("cup", "컵 경기")], max_length=10
                    ),
                ),
                ("match_date", models.DateField()),
            ],
            options={
                "verbose_name_plural": "Matches",
            },
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("photo", models.ImageField(upload_to="players/")),
                ("name", models.CharField(max_length=255)),
                ("nationality", models.CharField(max_length=255)),
                ("position", models.CharField(max_length=255)),
                ("detailed_position", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Players",
            },
        ),
        migrations.CreateModel(
            name="Stadium",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("grass_type", models.CharField(max_length=255)),
                ("capacity", models.PositiveIntegerField()),
                ("opening_date", models.DateField()),
            ],
            options={
                "verbose_name_plural": "Stadiums",
            },
        ),
    ]
