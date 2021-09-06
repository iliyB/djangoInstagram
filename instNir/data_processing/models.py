from django.urls import reverse
from djongo import models
from django.utils import timezone
from collections import namedtuple

DataAboutUser = namedtuple("DataAboutUser",
                           ["id",
                            "full_name",
                            "is_private",
                            "media_count",
                            "follower_count",
                            "following_count",
                            "biography",
                            "external_link",
                            "email", "phone",
                            "is_business",
                            "business_category",
                            "instagram_link",
                            "pic"])


class UserObject(models.Model):
    """
    Объект модели представляет собой документ, хранящий все данные о наблюдаемом пользователе

    Структура документа:

    username: string;
    activate: bool;
    id: integer;
    full_name: string;
    is_private: bool;
    media_count: int;
    follower_count: int;
    following_count: int;
    biography: string;
    external_link: string;
    email: string;
    phone: string;
    is_business: bool;
    business_category: string;
    instagram_link: string;
    last_update: datetime;
    is_updated: bool;
    pic: ImageField;


    medias: {
        id (int): {  - где id идентификатор ресурса в Instagram
            type: Union['photo', 'feed', 'igtv, 'clips', 'album']; - тип ресурса
            likes: int; - количество лайков
            comments: int; - количество комментариев
            date: datetime; - дата опубликования
            link: - ссылка на ресурс
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

    id = models.BigIntegerField(
        default=0,
        verbose_name="id пользователя в Instagram"
    )

    full_name = models.CharField(
        default="",
        verbose_name="Полное имя пользователя в Instagram",
        max_length=250
    )

    is_private = models.BooleanField(
        default=False,
        verbose_name="Приватный ли аккаунт"
    )

    media_count = models.IntegerField(
        default=0,
        verbose_name="Количество записей пользователя"
    )

    follower_count = models.IntegerField(
        default=0,
        verbose_name="Количество подписчиков пользователя"
    )

    following_count = models.IntegerField(
        default=0,
        verbose_name="Количество пользователей на которых подписан объект наблюдения"
    )

    biography = models.CharField(
        default="",
        max_length=500,
        verbose_name="Биография пользователя"
    )

    external_link = models.CharField(
        max_length=250,
        default="",
        verbose_name="Внешние ссылки пользователя"
    )

    email = models.CharField(
        max_length=50,
        default="",
        verbose_name="Email пользователя"
    )

    phone = models.CharField(
        max_length=30,
        default="",
        verbose_name="Телефон пользователя"
    )

    is_business = models.BooleanField(
        default=False,
        verbose_name="Является ли аккаунт бизнес аккаунтом"
    )

    business_category = models.CharField(
        max_length=200,
        default="",
        verbose_name="Категория бизнес аккаунта"
    )

    instagram_link = models.CharField(
        max_length=250,
        default="",
        verbose_name="Ссылка на аккаунт Instagram"
    )

    last_update = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Показывает время последнего обновление данных пользователя"
    )

    is_updated = models.BooleanField(
        default=True,
        verbose_name="Указывает, находится ли данные об аккаунте в процессе обновления"
    )
    
    pic = models.ImageField(
        upload_to="icon/",
        null=True,
        verbose_name="Хранит иконку профиля пользователя"
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
    
    def delete(self, using=None, keep_parents=False):
        if self.pic:
            self.pic.storage.delete(self.pic.name)
        super().delete()

    def get_absolute_url(self):
        return reverse('user_url', kwargs={'username': self.username, 'resource': 'all', 'filter':  'objects'})

    def get_delete_url(self):
        return reverse('delete_url', kwargs={'username': self.username})
    
    def get_medias_url(self):
        return reverse("user_medias_url", kwargs={"username": self.username})
