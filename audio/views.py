from rest_framework import generics
from .models import AudioFile
from .serializers import AudioFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from pydub import AudioSegment, silence
import speech_recognition as sr
import os

class AudioFileUploadView(generics.CreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    CHUNK_SIZE_MS = 30000  # Set your desired chunk size in milliseconds
    OUTPUT_DIR = 'audio_chunks/'  # Directory to store audio chunks

    def perform_create(self, serializer):
        audio_file = serializer.validated_data['audio_file']

        # Create the output directory if it doesn't exist
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        # Save the audio file to the output directory with a unique filename
        audio_file_path = os.path.join(self.OUTPUT_DIR, audio_file.name)
        with open(audio_file_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        audio = AudioSegment.from_mp3(audio_file_path)
        recognizer = sr.Recognizer()

        # Split the audio into chunks based on silence
        chunks = silence.split_on_silence(audio, min_silence_len=500, silence_thresh=-50)
        transcription = ""

        for i, chunk in enumerate(chunks):
            chunk_output_path = os.path.join(self.OUTPUT_DIR, f'chunk_{i}.wav')
            chunk.export(chunk_output_path, format="wav")

            with sr.AudioFile(chunk_output_path) as source:
                audio_data = recognizer.record(source)
            try:
                chunk_transcription = recognizer.recognize_google(audio_data)
                transcription += chunk_transcription + " "
            except sr.UnknownValueError:
                pass

        # Save the path to the uploaded audio file in the model
        serializer.save(audio_file_path=audio_file_path, transcription=transcription)

        # Include the audio_file_path in the response
        response_data = serializer.data
        response_data['audio_file_path'] = audio_file_path
        return JsonResponse(response_data)
