from django import forms
from data_processing.models import UserObject


class UserObjectForm(forms.ModelForm):
    """Форма для добавление нового наблюдаемого пользователя"""
    class Meta:
        model = UserObject
        fields = ['username']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_control'}),
        }

class DeleteUserForm(forms.Form):
    """Форма для удаления наблюдаемого пользователя"""
    username = forms.CharField(max_length=50)



