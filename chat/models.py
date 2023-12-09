from django.db import models


class ChatRoom(models.Model):
    team = models.ForeignKey(
        "team_info.Team", on_delete=models.CASCADE, related_name="messages"
    )

    def __str__(self):
        return self.team.name


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content}"
