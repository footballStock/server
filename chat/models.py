from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        verbose_name="Team name",
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content}"
