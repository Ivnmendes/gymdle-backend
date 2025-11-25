from django.core.management.base import BaseCommand
from exercises.services import get_today_exercises

class Command(BaseCommand):
    help = 'Define o exercício do dia de acordo com as regras de negócio.'

    def handle(self, *args, **options):
        normal_exercise, hard_exercise = get_today_exercises()

