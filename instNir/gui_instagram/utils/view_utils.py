from .dict import *
from .database import *

ALL = 'all'
MEDIA = 'media'
STORY = 'story'

OBJECTS = 'objects'
TYPES = 'types'
HASHTAGS = 'hashtags'
FRIENDS = 'friends'
LIKES = 'likes'
COMMENTS = 'comments'


def get_objects_from_media(username: str, filter: str) -> {}:
    if filter == OBJECTS:
        objects = get_short_dict(get_objects_of_medias(username=username), 20)
    elif filter == FRIENDS:
        objects = get_short_dict(get_medias_friends(username=username), 20)
    elif filter == HASHTAGS:
        objects = get_short_dict(get_medias_hashtags(username=username), 20)
    elif filter == TYPES:
        objects = get_short_dict(get_types_of_medias(username=username), 20)
    elif filter == LIKES:
        objects = get_short_dict(get_num_of_likes(username=username), 20)
    elif filter == COMMENTS:
        objects = get_short_dict(get_num_of_comments(username=username), 20)
    else:
        objects = {}

    objects = sorted_dict(objects)

    return objects


def get_objects_from_story(username: str, filter: str) -> {}:
    if filter == OBJECTS:
        objects = get_short_dict(get_objects_of_stories(username=username), 20)
    elif filter == FRIENDS:
        objects = get_short_dict(get_stories_friends(username=username), 20)
    elif filter == HASHTAGS:
        objects = get_short_dict(get_stories_hashtags(username=username), 20)
    elif filter == TYPES:
        objects = get_short_dict(get_types_of_stories(username=username), 20)
    else:
        objects = {}

    objects = sorted_dict(objects)

    return objects


def get_objects_from_all(username: str, filter: str) -> {}:
    objects = merge_dict(
        get_objects_from_media(username, filter),
        get_objects_from_story(username, filter)
    )

    objects = sorted_dict(objects)

    return objects


def get_title_from_filter(filter: str) -> [str]:
    if filter == OBJECTS:
        title = ['Метаданные пользователя']
    elif filter == FRIENDS:
        title = ['Отмеченные друзья пользователя']
    elif filter == HASHTAGS:
        title = ['Хэштеги пользователя']
    elif filter == TYPES:
        title = ['Типы ресурсов пользователя']
    elif filter == LIKES:
        title = ['Количество лайков пользователя']
    elif filter == COMMENTS:
        title = ['Количество комментариев пользователя']
    else:
        title = ['Empty']

    return title