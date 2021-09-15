# Описание проекта

Проект позволяет обрабатывать открытые данные пользователей социальной сети Instagram.

# Инструменты разработки

**Стек:**
- Linux
- Python 3.6
- Django 3.0.5
- Djongo (mongo)
- Celery
- [Highcharts JS](https://www.highcharts.com/)
- [Instagrapi](https://github.com/adw0rd/instagrapi)

# Установка

### 1. Установка зависимостей

    pip install -r requirements.txt

### 2. Установка параметров

Создать файл instNir/.env, в котором находятся параметры, необходимые для функционирования проекта:  

    INSTAGRAM_LOGIN=''
    INSTAGRAM_PASSWORD=''


### 3. Установка БД

В проекте используется БД Mongo:
    
    sudo apt install mongodb-server

Для функционирования Celery необходимо каждый раз запускать брокер Redis:

    sudo docker run -p 6379:6379 -d redis

### 4. Запуск проекта

    cd instNir
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

### 5. Запуск Celery

Запуск worker:

    cd instNir 
    celery -A config worker -l INFO -c 1

Для периодичного обновления данных о наблюдаемых пользователях необходимо запустить beat:

    cd instNir 
    celery -A config beat -l INFO
    
