from django.core.management.base import BaseCommand
from exercises.services import get_today_exercises

class Command(BaseCommand):
    help = 'Define o exercício do dia de acordo com as regras de negócio.'

    def handle(self, *args, **options):
        normal_exercise, hard_exercise = get_today_exercises()

        if normal_exercise:
            self.stdout.write(
                self.style.SUCCESS(f'Exercício do dia normal definido com sucesso: {normal_exercise.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Aviso: Não foi possível definir o exercício do dia normal. Nenhum candidato encontrado.')
            )
        if hard_exercise:
            self.stdout.write(
                self.style.SUCCESS(f'Exercício do dia difícil definido com sucesso: {hard_exercise.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Aviso: Não foi possível definir o exercício do dia difícil. Nenhum candidato encontrado.')
            )