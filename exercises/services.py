from .models import Exercises, ExerciseHistory
from django.db import transaction 

def _get_today_exercise(is_normal_mode):
    """
        Retorna um exercício aleatório que não foi realizado recentemente.
        Otimizado para usar a ordenação aleatória do banco de dados (ORDER BY RANDOM()).
    """
    recent_ids = ExerciseHistory.objects.get_recent_history_ids(limit=10, is_normal_mode=is_normal_mode) 
    available_exercises = Exercises.objects.get_available_for_today(excluded_ids=list(recent_ids), is_normal_mode=is_normal_mode)
    if available_exercises.count() == 0:
        available_exercises = Exercises.objects.all()
    try:
        selected_exercise = available_exercises.order_by('?').first() 
    except Exception:
        return None

    if selected_exercise is None:
        return None

    with transaction.atomic():
        Exercises.objects.reset_all_todays_exercises(is_normal_mode=is_normal_mode) 
        Exercises.objects.change_todays_exercise(selected_exercise.exerciseId, True, is_normal_mode=is_normal_mode)
        ExerciseHistory.objects.add_exercise_history(selected_exercise, is_normal_mode=is_normal_mode)

    return selected_exercise

def get_today_exercises():
    """
        Retorna os dois exercícios definidos para o dia.
    """
    normal_exercise = _get_today_exercise(is_normal_mode=True)
    hard_exercise = _get_today_exercise(is_normal_mode=False)
    return normal_exercise, hard_exercise