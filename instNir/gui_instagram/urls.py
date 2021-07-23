from django.urls import path
from .views import *


urlpatterns = [
    path('', Users.as_view(), name='users_url'),
    path('add/', Add.as_view(), name='add_url'),
    path('<str:username>/', User.as_view(), name='user_url')
]