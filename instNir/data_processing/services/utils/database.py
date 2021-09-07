from datetime import datetime
from django.core.files.base import ContentFile

from data_processing.models import UserObject, DataAboutUser


def get_username(user: UserObject) -> str:
    """Возращает username пользователя из его документа user"""
    return user.username


def get_user_like_obj(username: str) -> UserObject:
    """Возращает документ пользователя user из БД по его username"""
    return UserObject.objects.get(username=username)



def activate_user(username: str) -> None:
    """Активирует пользователя с данным username для обновления данных"""
    user = UserObject.objects.get(username=username)
    user.activate = True
    user.save()


def deactivate_user(username: str) -> None:
    """Деактивирует пользователя с данным username для обновления данных"""
    user = UserObject.objects.get(username=username)
    user.activate = False
    user.save()


def check_activate(username: str) -> bool:
    """Проверяет активность пользователя с данным username для обновления данных"""
    user = UserObject.objects.get(username=username)
    return user.activate


def get_usernames() -> [str]:
    """Возвращает список всех username наблюдаемых пользователей, находящихся в БД"""
    return [user.username for user in UserObject.objects.all()]


def update_time(username: str) -> None:
    """Обновляет время последнего обновления данных пользователя с данным username"""
    user = UserObject.objects.get(username=username)
    user.last_update = datetime.now()
    user.is_updated = False
    user.save()

def is_updated_set_true(username: str) -> None:
    """Устанавливает параметр, отвечающий за указание обновляются ли данные о пользователе, в значение True"""
    user = UserObject.objects.get(username=username)
    user.is_updated = True
    user.save()

def check_media(user: UserObject, id_media: str) -> bool:
    """Проверяет наличие ресурса с главное страницы с id_story в документе пользователя user"""
    return user.medias.get(id_media) is None


def check_story(user: UserObject, id_story: str) -> bool:
    """Проверяет наличие истории с id_story в документе пользователя user"""
    return user.stories.get(id_story) is None


def add_media(user: UserObject, id_media: str, media_type: str, likes: int, comments: int, objects: {}, hashtags: [],
              friends: [], datetime_: datetime, link: str) -> None:
    """Добавляет информацию о ресурсе с главной страницы в документ пользователя user"""
    user.medias.update({
                        id_media: {
                            'type': media_type,
                            'likes': likes,
                            'comments': comments,
                            'date': datetime_,
                            'link': link,
                            'objects': objects,
                            'hashtags': hashtags,
                            'friends': friends}
                        })
    user.save()


def add_story(user: UserObject, id_story: str, story_type: str, objects: {}, hashtags: [], friends: [],
              datetime_: datetime) -> None:
    """Добавляет информацию о ресурсе с истории в документ пользователя user"""
    user.stories.update({
                        id_story: {
                            'type': story_type,
                            'date': datetime_,
                            'objects': objects,
                            'hashtags': hashtags,
                            'friends': friends}
                        })
    user.save()

def set_info_about_user(username: str, info: DataAboutUser) -> None:
    """Сохраняет основную информация об аккаунте Instagram"""
    user = UserObject.objects.get(username=username)

    user.id = info.id
    user.full_name = info.full_name
    user.is_private = info.is_private
    user.media_count = info.media_count
    user.follower_count = info.follower_count
    user.following_count = info.following_count
    user.biography = info.biography
    user.external_link = info.external_link
    user.email = info.email
    user.phone = info.phone
    user.is_business = info.is_business
    user.business_category = info.business_category
    user.instagram_link = info.instagram_link
    if info.pic is not None:
        user.pic.save(f"account_pic_{username}.jpg", ContentFile(info.pic), save=True)
    user.save()

