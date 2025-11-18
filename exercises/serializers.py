from rest_framework import serializers
from .models import Exercises

class ExercisesSerializerWithoutPopularity(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = [
            'exerciseId', 'name', 'targetMuscles', 'bodyParts', 
            'equipments', 'secondaryMuscles', 'gifUrl', 'isTodaysExercise'
        ]


class ExercisesSerializerWithPopularity(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = [
            'exerciseId', 'name', 'targetMuscles', 'bodyParts', 
            'equipments', 'secondaryMuscles', 'gifUrl', 
            'isTodaysExercise', 'popularity'
        ]


class SimpleExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['exerciseId', 'name', 'gifUrl']


class ExercisesGuessWithoutPopularitySerializer(serializers.Serializer):
    targetMuscles = serializers.CharField(max_length=100)
    bodyparts = serializers.CharField(max_length=100)
    equipments = serializers.CharField(max_length=100)
    secondaryMuscles = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=10)
    grip = serializers.CharField(max_length=50)
    popularity = serializers.CharField(max_length=10)

class ExercisesGuessWithPopularitySerializer(serializers.Serializer):
    targetMuscles = serializers.CharField(max_length=100)
    bodyparts = serializers.CharField(max_length=100)
    equipments = serializers.CharField(max_length=100)
    secondaryMuscles = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=10)
    grip = serializers.CharField(max_length=50)
    popularity = serializers.CharField(max_length=10)


class GameGuessSerializer(serializers.Serializer):
    exerciseId = serializers.CharField(max_length=20)