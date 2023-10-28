# emotion_detection/serializers.py
from rest_framework import serializers
from .models import Emotion

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'text', 'emotion', 'timestamp']
