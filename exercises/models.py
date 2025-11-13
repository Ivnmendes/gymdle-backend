from django.db import models
from django.contrib.postgres.fields import ArrayField

from .managers import ExercisesManager, ExerciseHistoryManager

class Exercises(models.Model):

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"

    exerciseId = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    targetMuscles = ArrayField(models.CharField(max_length=50), default=list)
    bodyParts = models.CharField(max_length=200)
    equipments = models.CharField(max_length=100)
    secondaryMuscles = ArrayField(models.CharField(max_length=50), default=list)
    gifUrl = models.URLField(max_length=200)
    isTodaysExercise = models.BooleanField(default=False)

    objects = ExercisesManager()

    def __str__(self):
        return self.name
    

class ExerciseHistory(models.Model):

    class Meta:
        verbose_name = "Exercise History"
        verbose_name_plural = "Exercise Histories"

    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    performed_at = models.DateTimeField(auto_now_add=True)

    objects = ExerciseHistoryManager()
    
    def __str__(self):
        return f"{self.exercise.name} performed at {self.performed_at}"
    