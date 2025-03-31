from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Message model to store user messages and AI responses
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link message to a user
    message = models.TextField()  # Store the user's message
    response = models.TextField()  # Store the AI's response
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was created

    def __str__(self):
        return f"Message from {self.user.username} at {self.created_at}"

