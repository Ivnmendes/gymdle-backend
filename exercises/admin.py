from django.contrib import admin

from .models import Exercises, ExerciseHistory

@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('exerciseId', 'name', 'targetMuscles', 'bodyParts', 'equipments', 'type', 'grip', 'isTodaysExercise', 'isNormalMode')
    search_fields = ('exerciseId', 'name', 'targetMuscles', 'bodyParts', 'equipments', 'type', 'grip')
    list_filter = ('isTodaysExercise', 'isNormalMode')
    ordering = ('name',)

@admin.register(ExerciseHistory)
class ExerciseHistoryAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'isNormalMode', 'performedAt')
    list_filter = ('isNormalMode', 'performedAt')
    search_fields = ('exercise__name',)
    ordering = ('-performedAt',)