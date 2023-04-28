from django.contrib import admin

from .models import YamUser


@admin.register(YamUser)
class PostAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
