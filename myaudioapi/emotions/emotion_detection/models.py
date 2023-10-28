# emotion_detection/models.py
from django.db import models

class Emotion(models.Model):
    text = models.TextField()
    emotion = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
