import random

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models

# Лучше писать сериалайзер в отдельном слое, но тк он в этом проекте один, пишем его здесь
class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sentences
        fields = ['pk', 'tense', 'sentence']
    

class RandomSentence(APIView):
    def get(self, *args, **kwargs):
        all_sentences = models.Sentences.objects.all()
        random_sentence = random.choice(all_sentences)
        serialized_random_word = SentenceSerializer(random_sentence, many=False)
        return Response(serialized_random_word.data)