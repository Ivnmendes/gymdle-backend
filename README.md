# Gymdle

Repositório para o backend do Gymdle, uma aplicação de adivinhação de exercícios diários inspirada no Wordle.

## Tecnologias Utilizadas

- Python 3.x
- Django
- PostgreSQL
- Django REST Framework

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Ivnmendes/gymdle-backend.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd gymdle-backend
   ```

3. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

4. Instale as dependências:

   ```bash
    pip install -r gymdle-backend/requirements.txt

5. Configure o banco de dados no arquivo `settings.py`.

6. Aplique as migrações:

   ```bash
   python manage.py migrate
   ```

7. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

## Configurar tarefa diária

Para configurar a tarefa diária que define o exercício do dia, utilize o script `scripts/run_daily_exercise.sh`. Certifique-se de que o script tenha permissão de execução:

```bash
chmod +x scripts/run_daily_exercise.sh
```

Também configure o caminho correto para do diretório do projeto dentro do script.

Em seguida, você pode configurar um cron job para executar este script diariamente. Edite o crontab com o comando:

```bash
crontab -e
```

Adicione a seguinte linha para executar o script todos os dias às 00:00:

```bash
# Agenda para rodar todos os dias à 00:05 (5 minutos após a meia-noite)
5 0 * * * /caminho/completo/para/seu/projeto/run_daily_exercise.sh >> /tmp/cron_daily_log.log 2>&1
```
