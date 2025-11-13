from django.db import models

class ExercisesManager(models.Manager):

    def get_all_names(self):
        """Retorna um QuerySet contendo apenas os nomes de todos os exercícios."""
        return self.get_queryset().values_list('name', flat=True).order_by('name')

    def get_all_names_and_ids(self):
        """Retorna um QuerySet contendo IDs e nomes."""
        return self.get_queryset().values('exerciseId', 'name').order_by('name')

    def get_all_names_and_gifurls(self):
        """Retorna um QuerySet contendo nomes e URLs dos GIFs."""
        return self.get_queryset().values('name', 'gifUrl').order_by('name')
    
    def get_all_names_and_exerciseids(self):
        """Retorna um QuerySet contendo nomes e IDs dos exercícios."""
        return self.get_queryset().values('name', 'exerciseId').order_by('name')
    
    def get_todays_exercises(self):
        """Retorna um QuerySet contendo os exercícios marcados como 'isTodaysExercise'."""
        return self.get_queryset().filter(isTodaysExercise=True).order_by('name')
    
    def get_exercise_details(self, exercise_id):
        """Retorna um dicionário com os detalhes completos de um exercício específico."""
        return self.get_queryset().filter(exerciseId=exercise_id).values(
            'exerciseId', 'name', 'targetMuscles', 'bodyParts', 
            'equipments', 'secondaryMuscles', 'gifUrl', 'isTodaysExercise'
        ).first()
    
    def change_todays_exercise(self, exercise_id, is_today):
        """Altera o status 'isTodaysExercise' de um exercício específico."""
        return self.get_queryset().filter(exerciseId=exercise_id).update(isTodaysExercise=is_today)
    
    def search_exercises_by_name(self, search_term):
        """Retorna um QuerySet contendo exercícios cujo nome contém o termo de busca."""
        return self.filter(name__icontains=search_term).values('exerciseId', 'name').order_by('name')

    def search_by_muscle(self, muscle_name):
        """Retorna um QuerySet contendo exercícios que trabalham o músculo especificado."""
        return self.filter(
            models.Q(targetMuscles__icontains=muscle_name) | 
            models.Q(secondaryMuscles__icontains=muscle_name)
        ).values('exerciseId', 'name').order_by('name')
    
    def search_by_body_part(self, body_part):
        """Retorna um QuerySet contendo exercícios que envolvem a parte do corpo especificada."""
        return self.filter(bodyParts__icontains=body_part).values('exerciseId', 'name').order_by('name')
    
    def search_by_equipment(self, equipment):
        """Retorna um QuerySet contendo exercícios que utilizam o equipamento especificado."""
        return self.filter(equipments__icontains=equipment).values('exerciseId', 'name').order_by('name')
    
    def reset_all_todays_exercises(self):
        """Reseta o status 'isTodaysExercise' para False em todos os exercícios."""
        return self.get_queryset().update(isTodaysExercise=False)
    
    def count_total_exercises(self):
        """Retorna a contagem total de exercícios na base de dados."""
        return self.get_queryset().count()
    
    def get_available_for_today(self, excluded_ids):
        """Retorna QuerySet excluindo a lista de IDs de exercícios recentes."""
        return self.get_queryset().exclude(exerciseId__in=excluded_ids)
    
class ExerciseHistoryManager(models.Manager):

    def get_history_by_exercise(self, exercise_id):
        """Retorna um QuerySet contendo o histórico de um exercício específico."""
        return self.get_queryset().filter(exercise__exerciseId=exercise_id).order_by('-performed_at')
    
    def add_exercise_history(self, exercise):
        """Adiciona uma nova entrada ao histórico de exercícios."""
        history_entry = self.model(exercise=exercise)
        history_entry.save()
        return history_entry
    
    def clear_history(self):
        """Remove todas as entradas do histórico de exercícios."""
        return self.get_queryset().all().delete()
    
    def get_recent_history_ids(self, limit=10):
        """Retorna um QuerySet contendo as entradas mais recentes do histórico de exercícios."""
        return self.get_queryset().values_list('exercise__exerciseId', flat=True).order_by('-performed_at')[:limit]
    
    def get_history_count(self):
        """Retorna a contagem total de entradas no histórico de exercícios para cada exercício."""
        return self.get_queryset().values('exercise__exerciseId', 'exercise__name').annotate(
            count=models.Count('id')
        ).order_by('-count')