from django.urls import path

from config.diary.apps import DiaryConfig

app_name = DiaryConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    ]