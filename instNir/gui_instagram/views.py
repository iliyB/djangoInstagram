from django.shortcuts import render, redirect
from django.views import View
from .forms import UserObjectForm
from .models import UserObject
from .tasks import add_data_about_user


# Create your views here.

class Users(View):

    def get(self, request):
        users = UserObject.objects.all()
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

    def get(self, request, username):
        user = UserObject.objects.get(username=username)
        return render(request, 'gui_instagram/current_user.html', context={'user': user})


