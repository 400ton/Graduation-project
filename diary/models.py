from django.db import models
from pytils.translit import slugify

from users.models import User, NULLABLE


class Diary(models.Model):
    STATUS_CHOICES = (
        ('no_published', 'Не опубликовано'),
        ('moderation', 'На модерации'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    )
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, **NULLABLE)
    preview = models.ImageField(upload_to='media/diary/images', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', null=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='no_published', verbose_name="Статус")

    def __str__(self):
        return f'{self.title} {self.created_at} {self.views}'

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Diary.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Дневник'
        verbose_name_plural = 'Дневники'
        ordering = ['-created_at']
        permissions = [
            ('can_moderate', 'Может модерировать записи'),
        ]


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messages', **NULLABLE)
    name = models.CharField(max_length=200, **NULLABLE)
    email = models.EmailField(max_length=200, **NULLABLE)
    subject = models.CharField(max_length=200, **NULLABLE)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
