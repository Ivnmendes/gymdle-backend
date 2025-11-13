#!/bin/bash
PROJECT_DIR="/home/ubuntu/caminho/para/seu/projeto"
cd $PROJECT_DIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=gymdle.settings
python manage.py set_daily_exercise

deactivate