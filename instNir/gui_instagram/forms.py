from django import forms
from .models import UserObject


class UserObjectForm(forms.ModelForm):

    class Meta:
        model = UserObject
        fields = ['username']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_control'}),
        }

class DeleteUserForm(forms.Form):

    username = forms.CharField(max_length=50)



