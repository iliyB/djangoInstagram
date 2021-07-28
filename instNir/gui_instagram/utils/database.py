from ..models import UserObject
from datetime import datetime


def get_username(user: UserObject) -> str:
    return user.username


def get_user_like_obj(username: str) -> UserObject:
    return UserObject.objects.get(username=username)


def new_user(username: str) -> UserObject:
    user = UserObject()
    user.username = username
    user.save()
    return user


def activate_user(username: str):
    user = UserObject.objects.get(username=username)
    user.activate = True
    user.save()


def deactivate_user(username: str):
    user = UserObject.objects.get(username=username)
    user.activate = False
    user.save()


def check_activate(username: str) -> bool:
    user = UserObject.objects.get(username=username)
    return user.activate


def delete_user(username: str):
    user = UserObject.objects.get(username=username)
    user.delete()


def get_usernames() -> []:
    usernames = []
    for user in UserObject.objects.all():
        usernames.append(user.username)
    return usernames


def update_time(username: str):
    user = UserObject.objects.get(username=username)
    user.last_update = datetime.now()
    user.save()


def check_media(user: UserObject, id_media: str) -> bool:
    if user.medias.get(id_media) is None:
        return False
    else:
        return True


def check_story(user: UserObject, id_story: str) -> bool:
    if user.stories.get(id_story) is None:
        return False
    else:
        return True


def add_media(user: UserObject, id_media: str, media_type: str, likes: int, comments: int, objects: {}, hashtags: [],
              friends: [], datetime_: datetime, ):
    user.medias.update({id_media: {'type': media_type, 'likes': likes, 'comments': comments, 'date': datetime_,
                                   'objects': objects, 'hashtags': hashtags,
                                   'friends': friends}})
    user.save()


def add_story(user: UserObject, id_story: str, story_type: str, objects: {}, hashtags: [], friends: [],
              datetime_: datetime):
    user.stories.update({id_story: {'type': story_type, 'date': datetime_,
                                    'objects': objects, 'hashtags': hashtags,
                                    'friends': friends}})
    user.save()


def get_num_of_likes(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    likes = {}
    for media in user.medias:
        num_of_likes = user.medias.get(media).get('likes')
        if likes.get(num_of_likes) is None:
            likes.update({num_of_likes: 1})
        else:
            likes.update({num_of_likes: likes.get(num_of_likes) + 1})
    return likes


def get_num_of_comments(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    comments = {}
    for media in user.medias:
        num_of_comments = user.medias.get(media).get('comments')
        if comments.get(num_of_comments) is None:
            comments.update({num_of_comments: 1})
        else:
            comments.update({num_of_comments: comments.get(num_of_comments) + 1})
    return comments

def get_medias_hashtags(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    hashtags = {}
    for media in user.medias:
        for ht in user.medias.get(media).get('hashtags'):
            if hashtags.get(ht) is None:
                hashtags.update({ht: 1})
            else:
                hashtags.update({ht: hashtags.get(ht) + 1})
    return hashtags


def get_stories_hashtags(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    hashtags = {}
    for story in user.stories:
        for ht in user.stories.get(story).get('hashtags'):
            if hashtags.get(ht) is None:
                hashtags.update({ht: 1})
            else:
                hashtags.update({ht: hashtags.get(ht) + 1})
    return hashtags


def get_medias_friends(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    friends = {}
    for media in user.medias:
        for friend in user.medias.get(media).get('friends'):
            if friends.get(friend) is None:
                friends.update({friend: 1})
            else:
                friends.update({friend: friends.get(friend) + 1})
    return friends


def get_stories_friends(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    friends = {}
    for story in user.stories:
        for friend in user.stories.get(story).get('friends'):
            if friends.get(friend) is None:
                friends.update({friend: 1})
            else:
                friends.update({friend: friends.get(friend) + 1})
    return friends


def get_objects_of_stories(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    objects = {}
    for story in user.stories:
        for obj in user.stories.get(story).get('objects'):
            if objects.get(obj) is None:
                objects.update({obj: user.stories.get(story).get('objects').get(obj)})
            else:
                objects.update({obj: objects.get(obj) + user.stories.get(story).get('objects').get(obj)})
    return objects


def get_objects_of_medias(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    objects = {}
    for media in user.medias:
        for obj in user.medias.get(media).get('objects'):
            if objects.get(obj) is None:
                objects.update({obj: user.medias.get(media).get('objects').get(obj)})
            else:
                objects.update({obj: objects.get(obj) + user.medias.get(media).get('objects').get(obj)})
    return objects


def get_types_of_stories(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    types = {}
    for story in user.stories:
        if types.get(user.stories.get(story).get('type')) is None:
            types.update({user.stories.get(story).get('type'): 1})
        types.update({user.stories.get(story).get('type'): types.get(user.stories.get(story).get('type')) + 1})
    return types


def get_types_of_medias(username: str) -> {}:
    user = UserObject.objects.get(username=username)
    types = {}
    for media in user.medias:
        if types.get(user.medias.get(media).get('type')) is None:
            types.update({user.medias.get(media).get('type'): 1})
        else:
            types.update({user.medias.get(media).get('type'): types.get(user.medias.get(media).get('type')) + 1})
    return types
