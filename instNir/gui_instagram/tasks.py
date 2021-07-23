import sys

sys.path.append('..')
from instNir.celery import app
from gui_instagram.utils.InstagramClient import instagramUser
from gui_instagram.utils.database import *
from .login import LOGIN, PASSWORD



@app.task
def add_data_about_user(username: str):
    user = get_user_like_obj(username)
    instagramClient = instagramUser(LOGIN, PASSWORD)

    instagramClient.processing_resources_from_stories(user, 'media/')
    instagramClient.processing_resources_from_main_page(user, 'media/')



@app.task
def update_data_about_users():
    usernames = get_usernames()
    instagramClient = instagramUser(LOGIN, PASSWORD)

    for username in usernames:

        if not check_activate(username):
            continue

        user = get_user_like_obj(username)

        instagramClient.processing_resources_from_stories(user, '..media/')
        instagramClient.processing_resources_from_main_page(user, '..media/')

