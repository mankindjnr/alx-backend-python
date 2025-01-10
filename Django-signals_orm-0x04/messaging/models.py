from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    edited = models.BooleanField(default=False)  # Track if the message has been edited
    edited_at = models.DateTimeField(null=True, blank=True)  # When the message was edited
    edited_by = models.ForeignKey(User, related_name="edited_messages", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

class Notification(models.Model):
    notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message_id}"

class MessageHistory(models.Model):
    history_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(default=now)  # When the edit occurred

    def __str__(self):
        return f"History for Message {self.message.message_id}"