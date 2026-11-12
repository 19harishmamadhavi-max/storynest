from django.contrib import admin
from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'age_group')
    list_filter = ('age_group',)
    search_fields = ('title', 'author')
