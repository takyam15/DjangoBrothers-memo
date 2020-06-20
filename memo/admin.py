from django.contrib import admin

from .models import (
    Author, Memo
)


# Register your models here.

class MemoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_datetime', 'updated_datetime')
    list_display_links = ('id', 'title')


admin.site.register(Author)
admin.site.register(Memo, MemoAdmin)