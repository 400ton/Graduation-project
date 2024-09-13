from django.urls import path

from diary.apps import DiaryConfig
from diary.views import HomeListView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView, DiaryListView, \
    DiaryDetailView, DiaryModerationListView, DiaryModerationActionView

app_name = DiaryConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('moderation/', DiaryModerationListView.as_view(), name='moderation_list'),
    path('moderation/<slug:slug>/action/', DiaryModerationActionView.as_view(), name='moderation_action'),

    path('diary/', DiaryListView.as_view(), name='list'),
    path('create/', DiaryCreateView.as_view(), name='create'),
    path('<slug:slug>/', DiaryDetailView.as_view(), name='detail'),
    path('update/<slug:slug>/', DiaryUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', DiaryDeleteView.as_view(), name='delete'),


]
