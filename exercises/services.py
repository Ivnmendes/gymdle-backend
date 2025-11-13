from .models import Exercises, ExerciseHistory
from django.db import transaction 

def get_today_exercise():
    """
    Retorna um exercício aleatório que não foi realizado recentemente.
    Otimizado para usar a ordenação aleatória do banco de dados (ORDER BY RANDOM()).
    """
    recent_ids = ExerciseHistory.objects.get_recent_history_ids(limit=10) 
    available_exercises = Exercises.objects.get_available_for_today(excluded_ids=list(recent_ids))
    if available_exercises.count() == 0:
        available_exercises = Exercises.objects.all()
    try:
        selected_exercise = available_exercises.order_by('?').first() 
    except Exception:
        return None

    if selected_exercise is None:
        return None

    with transaction.atomic():
        Exercises.objects.reset_all_todays_exercises() 
        Exercises.objects.change_todays_exercise(selected_exercise.exerciseId, True)
        ExerciseHistory.objects.add_exercise_history(selected_exercise)

    return selected_exercise