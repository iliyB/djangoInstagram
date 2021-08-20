from enum import Enum


class Filter(Enum):
    OBJECTS = 'objects'
    TYPES = 'types'
    HASHTAGS = 'hashtags'
    FRIENDS = 'friends'
    LIKES = 'likes'
    COMMENTS = 'comments'


class SourceResource(Enum):
    ALL = 'all'
    MEDIA = 'media'
    STORY = 'story'


def get_title_from_filter(filter: Filter) -> [str]:
    """Возвращается title для графика по заданному filter"""

    if filter == Filter.OBJECTS:
        title = ['Метаданные пользователя']
    elif filter == Filter.FRIENDS:
        title = ['Отмеченные друзья пользователя']
    elif filter == Filter.HASHTAGS:
        title = ['Хэштеги пользователя']
    elif filter == Filter.TYPES:
        title = ['Типы ресурсов пользователя']
    elif filter == Filter.LIKES:
        title = ['Количество лайков пользователя']
    elif filter == Filter.COMMENTS:
        title = ['Количество комментариев пользователя']
    else:
        title = ['Empty']

    return title
