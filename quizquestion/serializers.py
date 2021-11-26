from rest_framework import serializers
from .models import QuizQuestion

class SaveQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'

       