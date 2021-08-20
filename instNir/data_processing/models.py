from django.urls import reverse
from djongo import models

from django.utils import timezone


class UserObject(models.Model):
    """
    Объект модели представляет собой документ, хранящий все данные о наблюдаемом пользователе

    Структура документа:

    username: string;
    activate: bool;
    last_update: datetime;

    medias: {
        id (int): {  - где id идентификатор ресурса в Instagram
            type: Union['photo', 'feed', 'igtv, 'clips', 'album']; - тип ресурса
            likes: int; - количество лайков
            comments: int; - количество комментариев
            date: datetime; - дата опубликования
            objects: [  - массив с объектами ресурса
                {
                  name: str;  - наименование объекта
                  count: int;   - количество таких объектов ресурса
                },
            ];
            hashtags: [name_hashtag: str]; - хештеги ресурса
            friends: [username: str]; - отмеченные пользователя ресурса
        }
    }

    stories: {
        id (int): {  - где id идентификатор ресурса в Instagram
            type: Union['photo', 'feed', 'igtv, 'clips']; - тип ресурса
            date: datetime; - дата опубликования
            objects: [  - массив с объектами ресурса
                {
                  name: str;  - наименование объекта
                  count: int;   - количество таких объектов ресурса
                },
            ];
            hashtags: [name_hashtag: str]; - хештеги ресурса
            friends: [username: str]; - отмеченные пользователя ресурса
        }
    }


    """


    username = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name='Ник наблюдаемого пользователя'
    )
    activate = models.BooleanField(
        default=True,
        verbose_name='Параметр, отвечающие за необходимость обновления данных о пользователе'
    )
    last_update = models.DateTimeField(
        default=timezone.now,
        verbose_name='Показывает время последнего обновление данных пользователя'
    )

    medias = models.JSONField(
        blank=True,
        default={},
        verbose_name='Хранит информацию об ресурсах с главной страницы'
    )
    stories = models.JSONField(
        blank=True,
        default={},
        verbose_name='Хранит информацию о ресурсах с историй'
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_url', kwargs={'username': self.username, 'resource': 'all', 'filter':  'objects'})

    def get_delete_url(self):
        return reverse('delete_url', kwargs={'username': self.username})
