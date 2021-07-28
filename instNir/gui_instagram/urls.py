from django.urls import path
from .views import *


urlpatterns = [
    path('', Users.as_view(), name='users_url'),
    path('add/', Add.as_view(), name='add_url'),
    path('<str:username>/delete', Delete.as_view(), name='delete_url'),
    path('<str:username>/<str:resource>/<str:filter>', User.as_view(), name='user_url')
]
