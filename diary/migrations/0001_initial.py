# Generated by Django 4.2 on 2024-09-06 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Описание')),
                ('slug', models.CharField(blank=True, max_length=150, null=True, verbose_name='Slug')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='media/diary/images', verbose_name='Изображение')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('is_published', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Дневник',
                'verbose_name_plural': 'Дневники',
            },
        ),
    ]
