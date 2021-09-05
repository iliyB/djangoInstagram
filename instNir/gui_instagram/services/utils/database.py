from collections import Counter

from data_processing.models import UserObject


def new_user(username: str) -> UserObject:
    """Создает нового наблюдаемого пользователя с заданным username"""
    user = UserObject()
    user.username = username
    user.save()
    return user


def delete_user(username: str) -> None:
    """Удаляет наблюдаемого пользователя с заданным username"""
    user = UserObject.objects.get(username=username)
    user.delete()


def get_usernames() -> [str]:
    """Возвращает список всех username наблюдаемых пользователей, находящихся в БД"""
    return [user.username for user in UserObject.objects.all()]




def get_num_of_likes(username: str) -> Counter:
    """
    Возвращает лайки ресурсов с главной страницы пользователя с заданным username
    Возвращает словарь вида:
    {
        'количество лайков': 'сколько раз было такое количество лайков',
    }
    """
    user = UserObject.objects.get(username=username)
    likes = Counter()
    for media in user.medias:
        num_of_likes = user.medias.get(media).get('likes')
        likes[num_of_likes] += 1
    return likes


def get_num_of_comments(username: str) -> Counter:
    """
    Возвращает комментарии ресурсов с главной страницы пользователя с заданным username
    Возвращает словарь вида:
    {
        'количество комментариев': 'сколько раз было такое количество комментариев',
    }
    """
    user = UserObject.objects.get(username=username)
    comments = Counter()
    for media in user.medias:
        num_of_comments = user.medias.get(media).get('comments')
        comments[num_of_comments] += 1
    return comments


def get_medias_hashtags(username: str) -> Counter:
    """
    Возвращает хештеги ресурсов с главной страницы пользователя с заданным username
    Возвращает словарь вида:
    {
        'хештег': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    hashtags = Counter()
    for media in user.medias:
        for hashtag in user.medias.get(media).get('hashtags'):
            hashtags[hashtag] += 1
    return hashtags


def get_stories_hashtags(username: str) -> Counter:
    """
    Возвращает лайки с историй пользователя с заданным username
    Возвращает словарь вида:
    {
        'количество лайков': 'сколько раз было такое количество лайков',
    }
    """
    user = UserObject.objects.get(username=username)
    hashtags = Counter()
    for story in user.stories:
        for hashtag in user.stories.get(story).get('hashtags'):
            hashtags[hashtag] += 1
    return hashtags


def get_medias_friends(username: str) -> Counter:
    """
    Возвращает отмеченные пользователи ресурсов с главной страницы пользователя с заданным username
    Возвращает словарь вида:
    {
        'username отмеченного пользователя': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    friends = Counter()
    for media in user.medias:
        for friend in user.medias.get(media).get('friends'):
            friends[friend] += 1
    return friends


def get_stories_friends(username: str) -> Counter:
    """
    Возвращает отмеченные пользователи с историй пользователя с заданным username
    Возвращает словарь вида:
    {
        'username отмеченного пользователя': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    friends = Counter()
    for story in user.stories:
        for friend in user.stories.get(story).get('friends'):
            friends[friend] += 1
    return friends


def get_stories_objects(username: str) -> Counter:
    """
    Возвращает объекты пользователи с историй пользователя с заданным username
    Возвращает словарь вида:
    {
        'имя объекта': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    objects = Counter()
    for story in user.stories:
        for object in user.stories.get(story).get('objects'):
            objects[object] += user.stories.get(story).get('objects').get(object)
    return objects


def get_medias_objects(username: str) -> Counter:
    """
    Возвращает объекты пользователи из ресурсов с главной страницы пользователя с заданным username
    Возвращает словарь вида:
    {
        'имя объекта': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    objects = Counter()
    for media in user.medias:
        for object in user.medias.get(media).get('objects'):
            objects[object] += user.medias.get(media).get('objects').get(object)
    return objects


def get_stories_types(username: str) -> Counter:
    """
    Возвращает типы ресурсов из историй пользователя с заданным username
    Возвращает словарь вида:
    {
        'тип истории': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    types = Counter()
    for story in user.stories:
        type = user.stories.get(story).get('type')
        types[type] += 1
    return types


def get_medias_types(username: str) -> Counter:
    """
    Возвращает типы ресурсов с главной страницы пользователя с заданным username
    Возвращает словарь вида:
    {
        'тип истории': 'сколько раз встречался',
    }
    """
    user = UserObject.objects.get(username=username)
    types = Counter()
    for media in user.medias:
        type = user.medias.get(media).get('type')
        types[type] += 1
    return types

def get_medias_links(username: str) -> [str]:
    """
    Возвращает ссылки на все медиа пользователя в виде списка
    """
    user = UserObject.objects.get(username=username)
    return [media.get('link') for media in user.medias]
