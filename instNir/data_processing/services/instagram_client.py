import os
import datetime
from enum import Enum
from collections import Counter
import requests
from typing import Optional

from instagrapi import Client

from data_processing.models import DataAboutUser
from data_processing.services.utils.detector import Detector
from data_processing.services.utils.file_utils import create_folder
from data_processing.services.utils.database import (
    check_media, check_story,
    add_media, add_story,
    get_user_like_obj,
    update_time,
    set_info_about_user,
    is_updated_set_true
)


class type_target(Enum):
    media = 0
    story = 1


class InstagramUser:
    """
    Класс отвечающий за полученние данных из социальной сети Instagram
    При инициализации логиниться в социальную сеть и загружает нейронные
    сети для определение объектов на ресурсах
    """

    def __init__(self, login: str, password: str, detection: bool = True) -> None:
        self.client = Client()
        self.client.login(login, password)
        print("Login in is successful")

        if detection:
            self.detector = Detector()

    def processing_resources_user(self, username: str, path: str = os.getcwd()):
        """Обрабатывает данные пользователя с заданным username с главной страницы и историй"""
        
        is_updated_set_true(username)
        set_info_about_user(username, self.get_info(username))
        self.processing_resources_from_main_page(username, path)
        self.processing_resources_form_stories(username, path)
        update_time(username)

    def get_info(self, username: str) -> DataAboutUser:
        """Возвращает основную информация о профиле Instagram в виде nametuple DataAboutUser"""
        user_id = self.client.user_id_from_username(username)
        info = self.client.user_info(user_id)

        return DataAboutUser(
            info.pk,
            info.full_name,
            info.is_private,
            info.media_count,
            info.follower_count,
            info.following_count,
            info.biography,
            info.external_url,
            info.public_email,
            info.contact_phone_number,
            info.is_business,
            info.business_category_name,
            "https://www.instagram.com/" + info.username + "/",
            self._download_profile_pict(info.profile_pic_url_hd)
        )

    def processing_resources_from_main_page(self, username: str, path: str = os.getcwd()):
        """Обрабатывает данные пользователя с заданным username с главной страницы"""

        user = get_user_like_obj(username)

        medias: [] = self._get_medias(username)
        path: str = self._create_folders(username, path, type_target.media)

        if not self.detector:
            print("Detector isn't define")

        for media in medias:

            if check_media(user, media.pk):
              continue

            print("New media")

            media_type: str = self._get_media_type_name(media)
            date_time: datetime = self._create_datetime_from_date_and_time(
                media.taken_at.date(),
                media.taken_at.time()
            )

            hashtags: [str] = self._get_hashtags_from_caption(media.caption_text)
            friends: [str] = self._get_media_friends(media)

            if not self.detector:
                objects = {}
            else:
                objects: {} = self._get_metadata_from_media(media, path)

            add_media(
                user,
                str(media.pk),
                media_type,
                int(media.like_count),
                int(media.comment_count),
                objects,
                hashtags,
                friends,
                date_time
            )

    def processing_resources_form_stories(self, username: str, path: str = os.getcwd()):
        """Обрабатывает данные пользователя с заданным username из историй"""

        user = get_user_like_obj(username)

        stories: [] = self._get_stories(username)
        path: str = self._create_folders(username, path, type_target.story)

        if not self.detector:
            print("Detector isn't define")

        for story in stories:

            if check_story(user, story.pk):
              continue

            print("New story")

            story_type: str = self._get_story_type_name(story)
            date_time: datetime = self._create_datetime_from_date_and_time(
                story.taken_at.date(),
                story.taken_at.time()
            )

            hashtags: [str] = []
            friends: [str] = self._get_story_friends(story)

            if not self.detector:
                objects = {}
            else:
                objects: {} = self._get_metadata_from_story(story, path)

            add_story(
                user,
                str(story.pk),
                story_type,
                objects,
                hashtags,
                friends,
                date_time
            )

    def _get_metadata_from_story(self, story, path: str) -> Counter:
        """Получает метаданные из истории, для этого история скачивается и обрабатывается нейронной сетью"""

        if story.media_type == 1:

            path_photo = self.client.story_download(story.pk, os.path.join(path, 'photo'))
            objects = self.detector.detector_photo.detector_objects_from_photo(str(path_photo), delete_file_=True)

        elif story.media_type == 2 and story.product_type == 'feed':

            path_video = self.client.story_download(story.pk, os.path.join(path, 'feed'))
            objects = self.detector.detector_video.detector_objects_from_video(str(path_video), delete_file_=True)

        elif story.media_type == 2 and story.product_type == 'igtv':

            path_video = self.client.story_download(story.pk, os.path.join(path, 'igtv'))
            objects = self.detector.detector_video.detector_objects_from_video(str(path_video), delete_file_=True)

        elif story.media_type == 2 and story.product_type == 'clips':

            path_video = self.client.story_download(story.pk, os.path.join(path, 'clips'))
            objects = self.detector.detector_video.detector_objects_from_video(str(path_video), delete_file_=True)

        return objects

    def _get_metadata_from_media(self, media, path: str) -> Counter:
        """Получает метаданные из медиа, для этого медиа скачивается и обрабатывается нейронной сетью"""

        if media.media_type == 1:

            path_photo = self.client.photo_download(media.pk, os.path.join(path, 'photo'))
            objects = self.detector.detector_photo.detector_objects_from_photo(str(path_photo), delete_file_=True)

        elif media.media_type == 2 and media.product_type == 'feed':

            path_video = self.client.video_download(media.pk, os.path.join(path, 'feed'))
            objects = self.detector.detector_video.detector_objects_from_video(str(path_video), delete_file_=True)

        elif media.media_type == 2 and media.product_type == 'igtv':

            path_video = self.client.video_download(media.pk, os.path.join(path, 'igtv'))
            objects = self.detector.detector_video.detector_objects_from_video(str(path_video), delete_file_=True)

        elif media.media_type == 2 and media.product_type == 'clips':

            path_video = self.client.video_download(media.pk, os.path.join(path, 'clips'))
            objects = self.detector.detector_video.detector_objects_from_video(str(path_video), delete_file_=True)

        elif media.media_type == 8:

            paths = self.client.album_download(media.pk, os.path.join(path, 'album'))

            objects = Counter()

            for path_media in paths:
                if str(path).find('.mp4'):
                    time_objects = self.detector.detector_video.detector_objects_from_video(
                        str(path_media),
                        delete_file_=True
                    )
                else:
                    time_objects = self.detector.detector_photo.detector_objects_from_photo(
                        str(path_media),
                        delete_file_=True
                    )
                objects += time_objects
        return objects

    def _get_stories(self, username: str) -> []:
        """Возвращает все истории пользователя с заданным username"""

        user_id = self.client.user_id_from_username(username)
        stories = self.client.user_stories(user_id)

        return stories

    def _get_medias(self, username) -> []:
        """Возвращает все ресурсы с главной страницы пользователя с заданным username"""

        user_id = self.client.user_id_from_username(username)
        medias = self.client.user_medias(user_id)

        return medias

    @staticmethod
    def _download_profile_pict(url_pic: str) -> Optional[bytes]:
        """Скачивает фотография профиля Instagram"""
        response = requests.get(url_pic)

        if not response.ok:
            return None

        return response.content

    @staticmethod
    def _get_story_friends(story) -> [str]:
        """Возвращает отмеченных пользователей в истории"""

        friends = []
        for usertag in story.mentions:
            friends.append((dict(dict(usertag).get('user'))['username']))

        return friends

    @staticmethod
    def _get_media_friends(media) -> [str]:
        """Возвращает отмеченных пользователей в медиа"""

        friends = []
        for usertag in media.usertags:
            friends.append((dict(dict(usertag).get('user'))['username']))

        return friends

    @staticmethod
    def _get_media_type_name(media) -> str:
        """Возвращает тип медиа в виде строки"""

        if media.media_type == 1:
            return "photo"
        if media.media_type == 8:
            return "album"

        return media.product_type

    @staticmethod
    def _get_story_type_name(story) -> str:
        """Возвращает тип истории в виде строки"""

        if story.media_type == 1:
            return "photo"

        return story.product_type

    @staticmethod
    def _create_datetime_from_date_and_time(date: datetime.date, time: datetime.time) -> datetime:
        """Создает datetime из date и time"""
        return datetime.datetime(year=date.year, month=date.month, day=date.day,
                        hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)

    @staticmethod
    def _get_hashtags_from_caption(caption: str) -> [str]:
        """Возвращает из caption media, используемые в ней хештеги"""

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

    @staticmethod
    def _create_folders(username: str, path: str, target: type_target) -> str:
        """
            Создает главную директорию пользователя с заданным username,
            отвечающего за хранение его ресурсов
            В зависимости от type_target создает и возвращает путь
            к директирии для историй или ресурсов с главной страницы
        """

        if not target.value:
            share_path = 'resources_from_main_page'
        else:
            share_path = 'resources_from_stories'

        create_folder(os.path.join(path, username))

        path = os.path.join(path, username, share_path)
        create_folder(path)

        create_folder(os.path.join(path, "photo"))
        create_folder(os.path.join(path, "feed"))
        create_folder(os.path.join(path, "igtv"))
        create_folder(os.path.join(path, "clips"))
        create_folder(os.path.join(path, "album"))

        return path