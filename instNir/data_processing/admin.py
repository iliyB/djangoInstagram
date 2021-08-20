from django.contrib import admin

from data_processing import models


@admin.register(models.UserObject)
class UserObjectAdmin(admin.ModelAdmin):
    list_display = ['username', 'activate', 'last_update']

