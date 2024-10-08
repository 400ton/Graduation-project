from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = 'Не указано'

    email = models.EmailField(unique=True, max_length=35, verbose_name='почта')
    avatar = models.ImageField(upload_to='media/users/avatars', verbose_name='аватар', **NULLABLE)
    num_phone = models.CharField(max_length=35, default='Не указано', verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, default='Не указано', verbose_name='страна', **NULLABLE)

    verification_code = models.CharField(max_length=100, verbose_name='код подтаерждения', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - активен:{self.is_active}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
