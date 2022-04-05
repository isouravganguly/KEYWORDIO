from dataclasses import field
from rest_framework import serializers
from rest_framework import book
from .models import book

class bookSerializer(serializers.ModelSerializer):
    class Meta:
        model = book
        field='_all_'
