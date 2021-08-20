from data_processing.models import UserObject
from datetime import datetime


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
    user.save()


def check_media(user: UserObject, id_media: str) -> bool:
    """Проверяет наличие ресурса с главное страницы с id_story в документе пользвоателя user"""
    return user.medias.get(id_media) is not None


def check_story(user: UserObject, id_story: str) -> bool:
    """Проверяет наличие истории с id_story в документе пользвоателя user"""
    return user.stories.get(id_story) is not None


def add_media(user: UserObject, id_media: str, media_type: str, likes: int, comments: int, objects: {}, hashtags: [],
              friends: [], datetime_: datetime, ) -> None:
    """Добавляет информацию о ресурсе с главной страницы в документ пользвоателя user"""
    user.medias.update({
                        id_media: {
                            'type': media_type,
                            'likes': likes,
                            'comments': comments,
                            'date': datetime_,
                            'objects': objects,
                            'hashtags': hashtags,
                            'friends': friends}
                        })
    user.save()


def add_story(user: UserObject, id_story: str, story_type: str, objects: {}, hashtags: [], friends: [],
              datetime_: datetime) -> None:
    """Добавляет информацию о ресурсе с истории в документ пользвоателя user"""
    user.stories.update({
                        id_story: {
                            'type': story_type,
                            'date': datetime_,
                            'objects': objects,
                            'hashtags': hashtags,
                            'friends': friends}
                        })
    user.save()