from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from data_processing.tasks import add_data_about_user
from data_processing.models import UserObject

from gui_instagram.forms import UserObjectForm, DeleteUserForm
from gui_instagram.services.view_utils import (
    get_objects_from_all, get_objects_from_story, get_objects_from_media,
)
from gui_instagram.services.filter import (
    Filter, SourceResource,
    get_title_from_filter,
)
from gui_instagram.services.utils.dict import convert_dict_to_plot_array

from django.conf import settings

class UserListView(ListView):
    """Выводит список наблюдаемых пользователей"""
    model = UserObject
    template_name = 'gui_instagram/users_list.html'


class AddUser(View):
    """Добавление нового наблюдаемого пользователя"""

    def get(self, request):
        form = UserObjectForm()
        #print(f"{settings.LOGIN} -  {settings.PASSWORD}")
        return render(request, 'gui_instagram/add_user.html', context={'form': form})

    def post(self, request):
        bound_form = UserObjectForm(request.POST)

        if bound_form.is_valid():
            new_form = bound_form.save()
            add_data_about_user.delay(new_form.username)
            return redirect('users_url')

        return render(request, 'gui_instagram/add_user.html', context={'form': bound_form})




class DetailUser(View):
    """Информация о пользователе: графики и тд"""

    def get(self, request, username, resource, filter):
        user = get_object_or_404(UserObject, username=username)
        filter = Filter(filter)

        context = {
            'user': user,
            'title': get_title_from_filter(filter),
            'resource': resource
        }
        resource = SourceResource(resource)

        if resource == SourceResource.ALL:
            objects = get_objects_from_all(username, filter)
            context.update({'objects': convert_dict_to_plot_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_all.html', context=context)
        elif resource == SourceResource.MEDIA:
            objects = get_objects_from_media(username, filter)
            context.update({'objects': convert_dict_to_plot_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_media.html', context=context)
        elif resource == SourceResource.STORY:
            objects = get_objects_from_story(username, filter)
            context.update({'objects': convert_dict_to_plot_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_story.html', context=context)
        else:
            objects = {}
            context.update({'objects': convert_dict_to_plot_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_all.html', context=context)
        



class DeleteUser(View):
    """Удаление наблюдаемого пользователя"""
    
    def get(self, request, username):
        form = DeleteUserForm()
        context = {
            'form': form,
            'username': username
        }
        return render(request, 'gui_instagram/delete_user.html', context=context)

    def post(self, request, username):
        form = DeleteUserForm(request.POST)

        if form.is_valid():
            if form.cleaned_data.get('username').lower() == username.lower():
                user = UserObject.objects.get(username=username)
                user.delete()
                return redirect('users_url')
            else:
                form.add_error(None, 'Wrong username')

        context = {
            'form': form,
            'username': username
        }
        return render(request, 'gui_instagram/delete_user.html', context=context)


