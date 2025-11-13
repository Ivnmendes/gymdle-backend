import json
from django.db import migrations

def convert_string_to_array(apps, schema_editor):
    Exercises = apps.get_model('exercises', 'Exercises')

    for exercise in Exercises.objects.all():
        needs_save = False

        if isinstance(exercise.targetMuscles, str):
            try:
                new_muscles = json.loads(exercise.targetMuscles)
                if isinstance(new_muscles, list):
                    exercise.targetMuscles = new_muscles
                    needs_save = True
            except json.JSONDecodeError:
                exercise.targetMuscles = []
                needs_save = True

        if isinstance(exercise.secondaryMuscles, str):
            try:
                new_muscles = json.loads(exercise.secondaryMuscles)
                if isinstance(new_muscles, list):
                    exercise.secondaryMuscles = new_muscles
                    needs_save = True
            except json.JSONDecodeError:
                exercise.secondaryMuscles = []
                needs_save = True
        
        if needs_save:
            exercise.save()


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_ultima_migracao_de_schema'),
    ]

    operations = [
        migrations.RunPython(convert_string_to_array, reverse_code=migrations.RunPython.noop),
    ]