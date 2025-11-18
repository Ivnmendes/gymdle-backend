from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    SimpleExercisesViewSet,
    ExercisesWithoutPopularityViewSet,
    ExercisesWithPopularityViewSet,
    EvaluateGameWithoutPopularityView,
    EvaluateGameWithPopularityView
)

router = SimpleRouter()

urlpatterns = router.urls + [
    path('exercises/simple/', SimpleExercisesViewSet.as_view({'get': 'list'}), name='simple-exercises'),
    # path('exercises/without-popularity/', ExercisesWithoutPopularityViewSet.as_view({'get': 'list'}), name='exercises-without-popularity'),
    # path('exercises/with-popularity/', ExercisesWithPopularityViewSet.as_view({'get': 'list'}), name='exercises-with-popularity'),
    path('exercises/evaluate-game/', EvaluateGameWithoutPopularityView.as_view(), name='evaluate-game'),
    # path('exercises/evaluate-game-full/', EvaluateGameWithPopularityView.as_view(), name='evaluate-game-full'),
]