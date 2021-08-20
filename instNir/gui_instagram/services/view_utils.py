from collections import Counter

from gui_instagram.services.utils.database import (
    get_stories_types, get_stories_objects, get_stories_friends, get_stories_hashtags,
    get_medias_types, get_medias_friends, get_medias_objects, get_medias_hashtags,
    get_num_of_likes, get_num_of_comments,
)
from gui_instagram.services.filter import Filter


def get_objects_from_media(username: str, filter: Filter, length_dir: int = 20) -> Counter:
    """Возвращает все объекты согласно filter для пользователя с заданным username из ресурсов с главной страницы"""

    if filter == Filter.OBJECTS:
        objects = get_medias_objects(username=username).most_common(length_dir)
    elif filter == Filter.FRIENDS:
        objects = get_medias_friends(username=username).most_common(length_dir)
    elif filter == Filter.HASHTAGS:
        objects =get_medias_hashtags(username=username).most_common(length_dir)
    elif filter == Filter.TYPES:
        objects = get_medias_types(username=username).most_common(length_dir)
    elif filter == Filter.LIKES:
        objects = get_num_of_likes(username=username).most_common(length_dir)
    elif filter == Filter.COMMENTS:
        objects = get_num_of_comments(username=username).most_common(length_dir)
    else:
        objects = []

    return Counter({k: v for k, v in objects})


def get_objects_from_story(username: str, filter: Filter, length_dir: int = 20) -> Counter:
    """Возвращает все объекты согласно filter для пользователя с заданным username из историй"""

    if filter == Filter.OBJECTS:
        objects = get_stories_objects(username=username).most_common(length_dir)
    elif filter == Filter.FRIENDS:
        objects = get_stories_friends(username=username).most_common(length_dir)
    elif filter == Filter.HASHTAGS:
        objects = get_stories_hashtags(username=username).most_common(length_dir)
    elif filter == Filter.TYPES:
        objects = get_stories_types(username=username).most_common(length_dir)
    else:
        objects = []

    return Counter({k: v for k, v in objects})


def get_objects_from_all(username: str, filter: Filter) -> Counter:
    """Возвращает все объекты согласно filter для пользователя с заданным username из всех ресурсов"""

    return get_objects_from_media(username, filter) + get_objects_from_story(username, filter)




