import sys

sys.path.append('..')
from instNir.celery import app
from gui_instagram.utils.InstagramClient import instagramUser
from gui_instagram.utils.database import *
from .login import LOGIN, PASSWORD



@app.task
def add_data_about_user(username: str):
    try:
        instagramClient = instagramUser(LOGIN, PASSWORD)

        instagramClient.processing_resources_from_stories(username, 'media/')
        instagramClient.processing_resources_from_main_page(username, 'media/')

        
    except Exception as e:
         print(e)



@app.task
def update_data_about_users():
    try:
        usernames = get_usernames()
        instagramClient = instagramUser(LOGIN, PASSWORD)
    except Exception as e:
        print(e)
    else:
        for username in usernames:
            try:
                if not check_activate(username):
                    continue

                instagramClient.processing_resources_from_stories(username, 'media/')
                instagramClient.processing_resources_from_main_page(username, 'media/')

            except Exception as e:
                print(e)

