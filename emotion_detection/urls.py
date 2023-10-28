# emotion_detection/urls.py
from django.urls import path
from .views import EmotionListCreateView, EmotionDetailView, TextEmotionDetectionView

urlpatterns = [
    path('emotions/', EmotionListCreateView.as_view(), name='emotion-list-create'),
    path('emotions/<int:pk>/', EmotionDetailView.as_view(), name='emotion-detail'),
    path('detect-emotion/', TextEmotionDetectionView.as_view(), name='detect-emotion'),
]
