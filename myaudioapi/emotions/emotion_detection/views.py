# emotion_detection/views.py
from rest_framework import generics, status
from transformers import pipeline
from .models import Emotion
from .serializers import EmotionSerializer
from rest_framework.response import Response

class EmotionListCreateView(generics.ListCreateAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

class EmotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

class TextEmotionDetectionView(generics.CreateAPIView):
    serializer_class = EmotionSerializer

    def create(self, request, *args, **kwargs):
        text = request.data.get('text')

        if not text:
            return Response({'error': 'Text field is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        # Load the emotion detection model
        emotion_pipeline = pipeline("sentiment-analysis", model="SamLowe/roberta-base-go_emotions")

        # Perform emotion detection
        result = emotion_pipeline(text)

        # Extract the emotion label
        emotion_label = result[0]['label']

        # Create a new Emotion instance and save it with the detected emotion
        emotion_instance = Emotion(text=text, emotion=emotion_label)
        emotion_instance.save()

        serializer = EmotionSerializer(emotion_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
