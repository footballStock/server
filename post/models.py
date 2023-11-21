from django.db import models
import os, datetime


class Post(models.Model):
    def image_directory_path(instance, filename):
        file = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return f'post/{instance.title}_image_{datetime.datetime.now().strftime("%Y_%m_%dT%H%M")}{extension}'

    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    image = models.ImageField(
        upload_to=image_directory_path,
        null=True,
        blank=True,
        default="post/default.jpg",
    )
    likes = models.ManyToManyField(
        "accounts.User", related_name="liked_posts", blank=True
    )
    dislikes = models.ManyToManyField(
        "accounts.User", related_name="disliked_posts", blank=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Report(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"Report on post '{self.post.title}' by {self.user.username}"
