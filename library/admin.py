from django.contrib import admin
from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'age_group')
    list_filter = ('category', 'age_group')
    search_fields = ('title', 'author')
