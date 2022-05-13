from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class progressSerializer(serializers.ModelSerializer):
    class Meta:
        model = testInProgress
        fields = '__all__'
