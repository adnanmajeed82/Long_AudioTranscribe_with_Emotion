from rest_framework import serializers
from .models import AudioFile

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'
        read_only_fields = ['audio_file_path']

    def create(self, validated_data):
        # Extract the audio_file from validated data
        audio_file = validated_data.pop('audio_file')

        # Create a new AudioFile instance without saving it yet
        audio_file_instance = AudioFile(**validated_data)

        # Save the audio file to the appropriate path
        audio_file_path = 'audio/' + audio_file.name  # Adjust the path as needed
        with open(audio_file_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Set the audio_file_path field and save the instance
        audio_file_instance.audio_file_path = audio_file_path
        audio_file_instance.save()

        return audio_file_instance
