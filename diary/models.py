from django.db import models
from config.users.models import User


class Diary(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Описание')
    slug = models.CharField(max_length=150, verbose_name='Slug', null=True, blank=True)
    preview = models.ImageField(upload_to='static/diary', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} {self.created_at} {self.views}'

    class Meta:
        verbose_name = 'Дневник'
        verbose_name_plural = 'Дневники'
