from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Exercises
from .serializers import (
    GameGuessSerializer,
    ExercisesSerializerWithoutPopularity,
    ExercisesSerializerWithPopularity,
    SimpleExercisesSerializer
)

# -- Funções auxiliares para comparação de atributos --
def normalize_input(value):
    """
    Converte QUALQUER entrada (List, String, Array Postgres, String JSON)
    para um set limpo de itens, removendo toda a formatação estrutural.
    """
    if value is None:
        return set()

    s_value = str(value)

    chars_to_remove = "[]{}'\""
    translation_table = str.maketrans('', '', chars_to_remove)
    
    cleaned_str = s_value.translate(translation_table)
    
    return set(item.strip().lower() for item in cleaned_str.split(',') if item.strip())

def compare_simple(guessed_value, correct_value):
    """ Comparação simples (ex: tipo, pegada) """
    status = 'wrong'
    normalized_guessed = normalize_input(guessed_value)
    normalized_correct = normalize_input(correct_value)
    
    print("\n\n\n", guessed_value, correct_value, "\n", normalized_guessed, normalized_correct , "\n\n\n")
    if normalized_guessed == normalized_correct:
        status = 'right'

    detail = list(normalized_guessed)
    if len(detail) == 1:
        detail = detail[0]
    elif len(detail) == 0:
        detail = ""

    return {
        "detail": detail,
        "status": status
    }

def compare(guessed_value, correct_value):
    """
    Comparação de listas/conjuntos (ex: targetMuscles, equipments).
    """
    g_set = normalize_input(guessed_value)
    c_set = normalize_input(correct_value)

    print("\n\n\n", guessed_value, correct_value, "\n", g_set, c_set , "\n\n\n")

    status = 'wrong'
    
    if g_set == c_set:
        status = 'right'
    elif not g_set.isdisjoint(c_set):
        status = 'partial'

    detail = list(g_set)
    
    if len(detail) == 1:
        detail = detail[0]

    return {
        "detail": detail,
        "status": status
    }

class SimpleExercisesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Rota simples: /api/exercises/simple/
    Retorna id, nome e gifUrl dos exercícios.
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
            guessed_exercise = Exercises.objects.get_exercise_details(exercise_id=guessed_exercise_id)
            correct_exercise = Exercises.objects.get_todays_exercises()
        except Exercises.DoesNotExist:
            return Response({'error': 'Exercício não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'exerciseId': guessed_exercise_id,
            'name': compare(guessed_exercise.get('name'), correct_exercise.get('name')),
            'gifUrl': guessed_exercise.get('gifUrl'),
            'targetMuscles': compare(guessed_exercise.get('targetMuscles'), correct_exercise.get('targetMuscles')),
            'bodyParts': compare(guessed_exercise.get('bodyParts'), correct_exercise.get('bodyParts')),
            'equipments': compare(guessed_exercise.get('equipments'), correct_exercise.get('equipments')),
            'secondaryMuscles': compare(guessed_exercise.get('secondaryMuscles'), correct_exercise.get('secondaryMuscles')),
            'type': compare_simple(guessed_exercise.get('type'), correct_exercise.get('type')),
            'grip': compare_simple(guessed_exercise.get('grip'), correct_exercise.get('grip')),
        }

        return Response(response_data, status=status.HTTP_200_OK)


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
            guessed_exercise = Exercises.objects.get_exercise_details(guessed_exercise_id)
            correct_exercise = Exercises.objects.get_todays_exercises()
        except Exercises.DoesNotExist:
            return Response({'error': 'Exercício não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'exerciseId': guessed_exercise_id,
            'name': compare(guessed_exercise.get('name'), correct_exercise.get('name')),
            'gifUrl': guessed_exercise.get('gifUrl'),
            'targetMuscles': compare(guessed_exercise.get('targetMuscles'), correct_exercise.get('targetMuscles')),
            'bodyParts': compare(guessed_exercise.get('bodyParts'), correct_exercise.get('bodyParts')),
            'equipments': compare(guessed_exercise.get('equipments'), correct_exercise.get('equipments')),
            'secondaryMuscles': compare(guessed_exercise.get('secondaryMuscles'), correct_exercise.get('secondaryMuscles')),
            'type': compare_simple(guessed_exercise.get('type'), correct_exercise.get('type')),
            'grip': compare_simple(guessed_exercise.get('grip'), correct_exercise.get('grip')),
            'popularity': compare_simple(guessed_exercise.get('popularity'), correct_exercise.get('popularity')),
        }

        return Response(response_data, status=status.HTTP_200_OK)