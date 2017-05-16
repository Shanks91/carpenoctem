from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_by")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_by")
    subject = models.CharField(max_length=250)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now=True)
    is_trash = models.BooleanField(default=False)

