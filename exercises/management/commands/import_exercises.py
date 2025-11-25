import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from exercises.models import Exercises
import os

class Command(BaseCommand):
    help = 'Importa exercícios de um arquivo JSON para o banco de dados.'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file', 
            type=str, 
            help='O caminho absoluto ou relativo para o arquivo JSON de exercícios.'
        )

    def handle(self, *args, **options):
        caminho_arquivo = options['json_file']
        
        if not os.path.exists(caminho_arquivo):
            raise CommandError(f'Arquivo não encontrado no caminho: {caminho_arquivo}')

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise CommandError('O arquivo JSON está mal formatado ou inválido.')
        except Exception as e:
            raise CommandError(f'Erro ao ler o arquivo: {e}')

        if not isinstance(data, list):
            raise CommandError('O arquivo JSON não contém uma lista de objetos.')

        self.stdout.write(f"Iniciando importação de {len(data)} exercícios...")
        
        objetos_criados = []
        erros_contagem = 0
        
        with transaction.atomic():
            for i, item in enumerate(data):
                try:
                    obj, created = Exercises.objects.update_or_create(
                    exerciseId=item['exerciseId'],
                    defaults={
                        'name': item.get('name', ''),
                        'targetMuscles': item.get('targetMuscles', []), 
                        'bodyParts': item.get('bodyParts', []),
                        'equipments': item.get('equipments', []),
                        'secondaryMuscles': item.get('secondaryMuscles', []),
                        'gifUrl': item.get('gifUrl', ''),
                        'type': item.get('type', 'outro'),
                        'grip': item.get('grip', 'nenhuma'),
                        'popularity': item.get('popularity', 'media'),
                        'instructions': item.get('instructions_pt', []),
                    }
                )
                    if created:
                        objetos_criados.append(obj)
                        
                except Exception as e:
                    erros_contagem += 1
                    self.stdout.write(self.style.ERROR(f"Erro na linha {i+1}: Falha ao criar/atualizar {item.get('name', 'N/A')}. Detalhe: {e}"))
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nProcesso concluído!"
            )
        )
        self.stdout.write(f"Total de objetos no JSON: {len(data)}")
        self.stdout.write(f"Objetos criados (novos): {len(objetos_criados)}")
        self.stdout.write(f"Objetos atualizados: {len(data) - len(objetos_criados) - erros_contagem}")
        self.stdout.write(f"Objetos com erros (ignorados): {erros_contagem}")