import instagrapi
import os
from enum import Enum
import datetime

from .detector import detector
from .checkPath import create_folder
from .dict import merge_dict
from .database import *
from ..models import UserObject


def get_hashtags_from_caption(caption: str) -> []:
    try:
        hashtags = []
        while caption.find("#"):
            hashtag = ""
            i = caption.index("#")
            while len(caption) > (i + 1) and caption[i + 1] != " " and caption[i + 1] != "\n":
                hashtag += caption[i + 1]
                i += 1

            hashtags.append(hashtag)
            caption = caption.replace("#", "", 1)
    except Exception:
        pass

    return hashtags


def create_datetime(date: datetime.date, time: datetime.time) -> datetime:
    return datetime(year=date.year, month=date.month, day=date.day,
                             hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)


class type_target(Enum):
    media = 0
    story = 1


class instagramUser():

    def __init__(self, login: str, password: str, detection=True):
        self.client = instagrapi.Client()
        self.client.login(login, password)
        print("Login in is successful")
        if detection:
            self.detector = detector()

    def create_folders(self, username: str, path: str, target: type_target) -> str:

        if not target.value:
            share_path = '/resources_from_main_page'
        else:
            share_path = '/resources_from_stories'

        create_folder(path + '/' + username)
        create_folder(path + '/' + username + share_path)

        path = path + "/" + username + share_path

        create_folder(path + "/photo")
        create_folder(path + "/feed")
        create_folder(path + "/igtv")
        create_folder(path + "/clips")
        create_folder(path + "/album")

        return path

    def processing_resources_from_main_page(self, username: str, path: str = os.getcwd()):

        user = get_user_like_obj(username)

        user_id = self.client.user_id_from_username(username)
        medias = self.client.user_medias(user_id)

        path = self.create_folders(username, path, type_target.media)

        if not self.detector:
            print("Detector isn't define. Medias will not be add")

        for media in medias:

            if check_media(user, media.pk):
                continue

            print("New media")

            if media.media_type == 1:
                type_media = 'photo'
            elif media.media_type == 8:
                type_media = 'album'
            else:
                type_media = str(media.product_type)

            date_time = create_datetime(media.taken_at.date(), media.taken_at.time())

            hashtags = get_hashtags_from_caption(media.caption_text)

            friends = []
            if media.usertags:
                for usertag in media.usertags:
                    friends.append((dict(dict(usertag).get('user'))['username']))

            if not self.detector:
                continue

            if media.media_type == 1:

                path_photo = self.client.photo_download(media.pk, path + '/photo')
                objects = self.detector.detector_photo.detectorRetinaNet_from_photo(str(path_photo), delete_file_=True)

            elif media.media_type == 2 and media.product_type == 'feed':

                path_video = self.client.video_download(media.pk, path + '/feed')
                objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_video), delete_file_=True)

            elif media.media_type == 2 and media.product_type == 'igtv':

                path_video = self.client.video_download(media.pk, path + '/igtv')
                objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_video), delete_file_=True)

            elif media.media_type == 2 and media.product_type == 'clips':

                path_video = self.client.video_download(media.pk, path + '/clips')
                objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_video), delete_file_=True)

            elif media.media_type == 8:

                paths = self.client.album_download(media.pk, path + '/album')

                objects = {}
                for path_media in paths:
                    if str(path).find('.mp4'):
                        time_objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_media),
                                                                                                 delete_file_=True)
                    else:
                        time_objects = self.detector.detector_photo.detectorRetinaNet_from_photo(str(path_media),
                                                                                                 delete_file_=True)
                    objects = merge_dict(objects, time_objects)

            add_media(user, str(media.pk), type_media, int(media.like_count), int(media.comment_count), objects, hashtags, friends, date_time)
        update_time(username)

    def processing_resources_from_stories(self, username: str, path: str = os.getcwd()):

        user = get_user_like_obj(username)

        user_id = self.client.user_id_from_username(username)
        stories = self.client.user_stories(user_id)

        path = self.create_folders(username, path, type_target.story)

        if not self.detector:
            print("Detector isn't define. Stories will not be add")

        for story in stories:

            if not check_story(user, story.pk):
                continue

            print("New Story")

            if story.media_type == 1:
                type_story = 'photo'
            else:
                type_story = str(story.product_type)

            date_time = create_datetime(story.taken_at.date(), story.taken_at.time())

            friends = []
            if story.mentions:
                for usertag in story.mentions:
                    friends.append((dict(dict(usertag).get('user'))['username']))

            if not self.detector:
                continue

            if story.media_type == 1:

                path_photo = self.client.photo_download_from_story(story.pk, path + '/photo')
                objects = self.detector.detector_photo.detectorRetinaNet_from_photo(str(path_photo), delete_file_=True)

            elif story.media_type == 2 and story.product_type == 'feed':

                path_video = self.client.video_download_from_story(story.pk, path + '/feed')
                objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_video), delete_file_=True)

            elif story.media_type == 2 and story.product_type == 'igtv':

                path_video = self.client.video_download_from_story(story.pk, path + '/igtv')
                objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_video), delete_file_=True)

            elif story.media_type == 2 and story.product_type == 'clips':

                path_video = self.client.video_download_from_story(story.pk, path + '/clips')
                objects = self.detector.detector_video.detectorRetinaNet_from_video(str(path_video), delete_file_=True)

            add_story(user, str(story.pk), type_story, objects, [], friends, date_time)
        update_time(username)
