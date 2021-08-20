from django.conf import settings
from config.celery import app

from data_processing.services.instagram_client import InstagramUser
from data_processing.services.utils.database import get_usernames, check_activate


@app.task
def add_data_about_user(username: str):
    """Обрабатывает информацию о пользователи из социлаьной сети при инициализации этоо пользователя"""
    try:

        instagramClient = InstagramUser(settings.ENV_CONFIG.get("INSTAGRAM_LOGIN"), settings.ENV_CONFIG.get("INSTAGRAM_PASSWORD"))

        instagramClient.processing_resources_user(username, 'media/')

    except Exception as e:
        print(e)


@app.task
def update_data_about_users():
    """Обновляет данные пользователей из социальной сети"""
    try:
        usernames = get_usernames()
        instagramClient = InstagramUser(settings.ENV_CONFIG.get("INSTAGRAM_LOGIN"), settings.ENV_CONFIG.get("INSTAGRAM_PASSWORD"))
    except Exception as e:
        print(e)
    else:
        for username in usernames:
            try:
                if not check_activate(username):
                    continue

                instagramClient.processing_resources_user(username, 'media/')

            except Exception as e:
                print(e)
