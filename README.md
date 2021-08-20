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
- [Imageai](https://imageai.readthedocs.io/en/latest/)
- [Instagrapi](https://github.com/adw0rd/instagrapi)

# Установка

### 1. Установка зависимостей

    pip install -r requirements.txt

В проекте используются нейронные сети для определение метаданных с ресурсов из социальной сети Instagram.  
Желательно использовать CUDA ядра (работает намного быстрее) для нейронной сети.  
Для imageai, при использовании CUDA ядер, необходимо cuDNN=8.0 и CUDA=11.0.
    
    pip install tensorflow-gpu==2.4.0

При отсутствии CUDA ядер:

    pip install tensorflow==2.4.0

### 2. Установка параметров

В файле instNir/.env находятся параметры, необходимые для функционирования проекта:  

    INSTAGRAM_LOGIN=''
    INSTAGRAM_PASSWORD=''
    PATH_TO_RETINA_NET_MODEL=''

В ___PATH_TO_RETINA_NET_MODEL___ находится путь до модели нейронной сети RetinaNet, которую можно скачать по [ссылке](https://imageai.readthedocs.io/en/latest/detection/).  

### 3. Установка БД

В проекте используется БД Mongo:
    
    sudo apt install mongodb-server

Для функционирования Celery необходимо каждый раз запускать брокер Redis:

    sudo docker run -p 6379:6379 -d redis

### 4. Запуск проекта

    cd instNir
    python manage.py makemigrations
    python manage.py migrate
    pythom manage.py runserver

### 5. Запуск Celery

Запуск worker:

    cd instNir 
    celery -A config worker -l INFO

Для периодичного обновления данных о наблюдаемых пользователях необходимо запустить beat:

    cd instNir 
    celery -A config beat -l INFO
    
