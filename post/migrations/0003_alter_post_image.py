# Generated by Django 4.2.6 on 2023-11-20 13:41

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0002_post_dislikes_post_likes_report"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=post.models.Post.image_directory_path
            ),
        ),
    ]
