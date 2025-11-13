from django.core.management.base import BaseCommand
from exercises.services import get_today_exercise

class Command(BaseCommand):
    help = 'Define o exercício do dia de acordo com as regras de negócio.'

    def handle(self, *args, **options):
        exercise = get_today_exercise()

        if exercise:
            self.stdout.write(
                self.style.SUCCESS(f'Exercício do dia definido com sucesso: {exercise.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Aviso: Não foi possível definir o exercício do dia. Nenhum candidato encontrado.')
            )