from django.urls import path

from diary.apps import DiaryConfig
from diary.views import HomeListView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView, DiaryListView, \
    DiaryDetailView

app_name = DiaryConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('diary', DiaryListView.as_view(), name='list_diary'),
    path('detail/<int:pk>', DiaryDetailView.as_view(), name='detail'),
    path('create/', DiaryCreateView.as_view(), name='create'),
    path('update/<int:pk>', DiaryUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', DiaryDeleteView.as_view(), name='delete')
]
