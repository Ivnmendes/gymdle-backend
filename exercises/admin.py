from django.contrib import admin

from .models import Exercises, ExerciseHistory

@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('exerciseId', 'name', 'targetMuscles', 'bodyParts', 'equipments', 'isTodaysExercise')
    search_fields = ('exerciseId', 'name', 'targetMuscles', 'bodyParts', 'equipments')
    list_filter = ('isTodaysExercise',)
    ordering = ('name',)

@admin.register(ExerciseHistory)
class ExerciseHistoryAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'performed_at')
    search_fields = ('exercise__name',)
    ordering = ('-performed_at',)