from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users_url'),
    path('add/', views.AddUser.as_view(), name='add_url'),
    path("<str:username>/medias", views.DetailUserMedias.as_view(), name="user_medias_url"),
    # path("<str:username>/stories", views.DetailUserStories.as_view(), name="user_stories_url"),
    path('<str:username>/delete', views.DeleteUser.as_view(), name='delete_url'),
    path('<str:username>/update', views.UpdateUser.as_view(), name='update_url'),
    path('<str:username>/<str:resource>/<str:filter>', views.DetailUser.as_view(), name='user_url'),
]
