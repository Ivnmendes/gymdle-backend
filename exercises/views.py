from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .managers import ExercisesManager
from .models import Exercises
from .serializers import (
    GameGuessSerializer,
    ExercisesSerializerWithoutPopularity,
    ExercisesSerializerWithPopularity,
    SimpleExercisesSerializer
)


class SimpleExercisesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Rota simples: /api/exercises/simple/
    Retorna id, nome e gifUrl dos exercicios.
    """
    queryset = Exercises.objects.filter(popularity='alta')
    serializer_class = SimpleExercisesSerializer


class ExercisesWithPopularityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Rota com popularidade: /api/exercises/with-popularity/
    Retorna todos os campos do exercicio, incluindo popularidade.
    """
    queryset = Exercises.objects.all()
    serializer_class = ExercisesSerializerWithPopularity
    lookup_field = 'exerciseId'

class ExercisesWithoutPopularityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Rota sem popularidade: /api/exercises/without-popularity/
    Retorna todos os campos do exercicio, exceto popularidade.
    """
    queryset = Exercises.objects.all()
    serializer_class = ExercisesSerializerWithoutPopularity
    lookup_field = 'exerciseId'


class EvaluateGameWithoutPopularityView(APIView):
    """
    Rota para avaliar o palpite de um exercício (sem popularidade).
    Compara o 'exerciseId' enviado com o exercício do dia.
    """
    def post(self, request, *args, **kwargs):
        serializer = GameGuessSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        guessed_exercise_id = serializer.validated_data['exerciseId']

        try:
            guessed_exercise = ExercisesManager.get_exercise_details(guessed_exercise_id)
            correct_exercise = ExercisesManager.get_todays_exercises()
        except Exercises.DoesNotExist:
            return Response({'error': 'Exercício não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'exerciseId': guessed_exercise_id,
            'gifUrl': guessed_exercise.get('gifUrl'),
            'targetMuscles': self.compare(guessed_exercise.get('targetMuscles'), correct_exercise.get('targetMuscles')),
            'bodyParts': self.compare(guessed_exercise.get('bodyParts'), correct_exercise.get('bodyParts')),
            'equipments': self.compare(guessed_exercise.get('equipments'), correct_exercise.get('equipments')),
            'secondaryMuscles': self.compare(guessed_exercise.get('secondaryMuscles'), correct_exercise.get('secondaryMuscles')),
            'type': self.compare_simple(guessed_exercise.get('type'), correct_exercise.get('type')),
            'grip': self.compare_simple(guessed_exercise.get('grip'), correct_exercise.get('grip')),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def compare_simple(self, guessed_value, correct_value):
        """ Comparação simples (string vs string) """
        status = 'wrong'
        if str(guessed_value).lower() == str(correct_value).lower():
            status = 'right'

        return {
            "detail": guessed_value,
            "status": status
        }

    def compare(self, guessed_values: list, correct_values: list):
        """
        Comparação de listas (ex: targetMuscles).
        Verifica se há sobreposição.
        """
        g_set = set(str(val).lower() for val in (guessed_values or []))
        c_set = set(str(val).lower() for val in (correct_values or []))

        status = 'wrong'
        
        if g_set == c_set:
            status = 'right'
        elif g_set.intersection(c_set):
            status = 'partial'

        return {
            "detail": guessed_values,
            "status": status
        }


class EvaluateGameWithPopularityView(APIView):
    """
    Rota para avaliar o palpite de um exercício (COM popularidade).
    Compara o 'exerciseId' enviado com o exercício do dia.
    """
    def post(self, request, *args, **kwargs):
        serializer = GameGuessSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        guessed_exercise_id = serializer.validated_data['exerciseId']

        try:
            guessed_exercise = ExercisesManager.get_exercise_details(guessed_exercise_id)
            correct_exercise = ExercisesManager.get_todays_exercises()
        except Exercises.DoesNotExist:
            return Response({'error': 'Exercício não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'exerciseId': guessed_exercise_id,
            'gifUrl': guessed_exercise.get('gifUrl'),
            'targetMuscles': self.compare(guessed_exercise.get('targetMuscles'), correct_exercise.get('targetMuscles')),
            'bodyParts': self.compare(guessed_exercise.get('bodyParts'), correct_exercise.get('bodyParts')),
            'equipments': self.compare(guessed_exercise.get('equipments'), correct_exercise.get('equipments')),
            'secondaryMuscles': self.compare(guessed_exercise.get('secondaryMuscles'), correct_exercise.get('secondaryMuscles')),
            'type': self.compare_simple(guessed_exercise.get('type'), correct_exercise.get('type')),
            'grip': self.compare_simple(guessed_exercise.get('grip'), correct_exercise.get('grip')),
            'popularity': self.compare_simple(guessed_exercise.get('popularity'), correct_exercise.get('popularity')),
        }

        return Response(response_data, status=status.HTTP_200_OK)


    def compare_simple(self, guessed_value, correct_value):
        """ Comparação simples (string vs string) """
        status = 'wrong'
        if str(guessed_value).lower() == str(correct_value).lower():
            status = 'right'

        return {
            "detail": guessed_value,
            "status": status
        }

    def compare(self, guessed_values: list, correct_values: list):
        """
        Comparação de listas (ex: targetMuscles).
        Verifica se há sobreposição.
        """
        g_set = set(str(val).lower() for val in (guessed_values or []))
        c_set = set(str(val).lower() for val in (correct_values or []))

        status = 'wrong'
        
        if g_set == c_set:
            status = 'right'
        elif g_set.intersection(c_set):
            status = 'partial'

        return {
            "detail": guessed_values,
            "status": status
        }