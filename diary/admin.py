from django.contrib import admin
from diary.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'owner')
    prepopulated_fields = {'slug': ('title',)}
