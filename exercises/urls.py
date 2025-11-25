from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    SimpleExercisesViewSet,
    ExercisesWithoutPopularityViewSet,
    ExercisesWithPopularityViewSet,
    EvaluateGameWithoutPopularityView,
    EvaluateGameWithPopularityView,
    HintTodayGameViewSet,
)

router = SimpleRouter()

urlpatterns = router.urls + [
    path('exercises/simple/', SimpleExercisesViewSet.as_view({'get': 'list'}), name='simple-exercises'),
    path('exercises/without-popularity/', ExercisesWithoutPopularityViewSet.as_view({'get': 'list'}), name='exercises-without-popularity'),
    path('exercises/with-popularity/', ExercisesWithPopularityViewSet.as_view({'get': 'list'}), name='exercises-with-popularity'),
    path('exercises/evaluate-game/', EvaluateGameWithoutPopularityView.as_view(), name='evaluate-game'),
    # path('exercises/evaluate-game-full/', EvaluateGameWithPopularityView.as_view(), name='evaluate-game-full'),
    path('exercises/hint/body-part/', HintTodayGameViewSet.as_view({'get': 'hint_body_parts'}), name='hint-today-game-body-parts'),
    path('exercises/hint/instructions/', HintTodayGameViewSet.as_view({'get': 'hint_instructions'}), name='hint-today-game-instructions'),
    path('exercises/hint/gif-url/', HintTodayGameViewSet.as_view({'get': 'hint_gif_url'}), name='hint-today-game-gif-url'),
]