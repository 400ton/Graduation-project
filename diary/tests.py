from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.core import mail
from diary.models import Diary
from users.models import User


class DiaryDetailViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email='testuser@example.com', password='testpassword')

        # Создаем опубликованную запись
        self.published_diary = Diary.objects.create(
            title='Test Published Diary',
            content='Content of the published diary',
            owner=self.user,
            is_published=True,
            views=99
        )

        # Создаем неопубликованную запись
        self.unpublished_diary = Diary.objects.create(
            title='Test Unpublished Diary',
            content='Content of the unpublished diary',
            owner=self.user,
            is_published=False,
            views=0
        )

    def test_published_diary_view_counter(self):
        """Проверка увеличения счетчика просмотров для опубликованной записи"""
        response = self.client.get(reverse('diary:detail', kwargs={'slug': self.published_diary.slug}))
        self.published_diary.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.published_diary.views, 100)

    def test_unpublished_diary_access_by_owner(self):
        """Проверка доступа к неопубликованной записи владельцем"""
        log = self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('diary:detail', kwargs={'slug': self.unpublished_diary.slug}))
        # Добавляем вывод информации для отладки
        print(f'Логин - {log}')
        self.assertEqual(response.status_code, 200)

    def test_unpublished_diary_access_by_another_user(self):
        """Проверка отказа в доступе к неопубликованной записи другим пользователем"""
        User.objects.create(email='anotheruser@example.com', password='testpassword')
        self.client.login(email='anotheruser@example.com', password='testpassword')
        response = self.client.get(reverse('diary:detail', kwargs={'slug': self.unpublished_diary.slug}))
        self.assertEqual(response.status_code, 403)  # Permission Denied

    def test_send_email_on_100_views(self):
        """Проверка отправки уведомления при достижении 100 просмотров"""
        self.client.get(reverse('diary:detail', kwargs={'slug': self.published_diary.slug}))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Уведомление', mail.outbox[0].subject)
        self.assertIn(self.published_diary.owner.email, mail.outbox[0].to)

    def test_post_request_changes_status_to_moderation(self):
        """Проверка, что POST запрос изменяет статус записи на 'moderation'"""
        self.client.login(email='testuser@example.com', password='testpassword')
        self.client.post(reverse('diary:detail', kwargs={'slug': self.published_diary.slug}),
                                    {'publish': True})
        self.published_diary.refresh_from_db()
        self.assertEqual(self.published_diary.status, 'moderation')

