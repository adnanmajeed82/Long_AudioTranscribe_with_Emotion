from django.db import models

class AudioFile(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/')  # Use FileField to store the audio file
    audio_file_path = models.CharField(max_length=255, blank=True)  # Use CharField to store the path
    transcription = models.TextField(blank=True)
     
    def __str__(self):
        return self.title