from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .forms import UserObjectForm, DeleteUserForm
from .models import UserObject
from .tasks import add_data_about_user
from .utils.database import *
from .utils.dict import convert_dict_to_array
from .utils.view_utils import *


# Create your views here.

class Users(View):

    def get(self, request):
        users = UserObject.objects.all()
        #users = get_list_or_404(UserObject)
        return render(request, 'gui_instagram/users.html', context={'users': users})



class Add(View):

    def get(self, request):
        form = UserObjectForm()
        return render(request, 'gui_instagram/add.html', context={'form': form})

    def post(self, request):
        bound_form = UserObjectForm(request.POST)

        if bound_form.is_valid():
            new_form = bound_form.save()
            add_data_about_user.delay(new_form.username)
            return redirect('users_url')

        return render(request, 'gui_instagram/add.html', context={'form': bound_form})




class User(View):

    def get(self, request, username, resource, filter):
        user = get_object_or_404(UserObject, username=username)

        context = {
            'user': user,
            'title': get_title_from_filter(filter),
            'resource': resource
        }

        if resource == ALL:
            objects = get_objects_from_all(username, filter)
            context.update({'objects': convert_dict_to_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_all.html', context=context)
        elif resource == MEDIA:
            objects = get_objects_from_media(username, filter)
            context.update({'objects': convert_dict_to_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_media.html', context=context)
        elif resource == STORY:
            objects = get_objects_from_story(username, filter)
            context.update({'objects': convert_dict_to_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_story.html', context=context)
        else:
            objects = {}
            context.update({'objects': convert_dict_to_array(objects)})
            return render(request, 'gui_instagram/current_user/current_user_all.html', context=context)
        



class Delete(View):
    
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


