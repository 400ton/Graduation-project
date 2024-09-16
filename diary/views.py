from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from config.settings import EMAIL_HOST_USER
from diary.forms import DiaryForm, DiaryUpdateForm
from diary.models import Diary


class HomeListView(ListView):
    """
    Представление для отображения главной страницы с опубликованными записями.
    - queryset: выбираются только записи со статусом is_published=True.
    """
    model = Diary
    template_name = "diary/home.html"
    paginate_by = 10

    def get_queryset(self):
        return Diary.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный дневник'
        return context


class DiaryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка заметок текущего пользователя.
    - queryset: выбираются записи только для владельца (request.user).
    """
    model = Diary
    template_name = 'diary/diary_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Diary.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список заметок'
        return context


class DiaryDetailView(DetailView):
    """
    Представление для отображения деталей записи.
    - При каждом просмотре запись увеличивает счетчик просмотров.
    - Если просмотров более 100, отправляется уведомление.
    - При POST запросе запись может быть отправлена на модерацию.
    - Опубликованная запись доступна всем пользователям (включая неавторизованных).
    - Неопубликованная запись доступна только владельцу.
    """
    model = Diary
    template_name = 'diary/diary_detail.html'

    def get_object(self, queryset=None):
        """
        Получает объект записи, увеличивает счетчик просмотров,
        если запись опубликована. Если количество просмотров >= 100,
        отправляется уведомление владельцу записи.
        """
        diary = super().get_object(queryset)

        # Проверка доступа
        if not diary.is_published and (self.request.user != diary.owner):
            raise PermissionDenied("У вас нет доступа к этой записи.")

        # Счетчик просмотров только для опубликованных записей
        if diary.is_published:
            Diary.objects.filter(pk=diary.pk).update(views=F('views') + 1)
            diary.refresh_from_db()

        # Уведомление владельцу
        if diary.views >= 100:
            html_message = render_to_string('diary/emails/email_notification.html',
                                            {'title': diary.title})
            plain_message = strip_tags(html_message)

            send_mail(
                subject='Уведомление',
                message=plain_message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[diary.owner.email],
                html_message=html_message
            )
        return diary

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос. Если пользователь отправляет запрос на публикацию записи,
        статус записи изменяется на "moderation".
        """
        diary = self.get_object()
        if 'publish' in request.POST:
            diary.status = 'moderation'
            diary.save()
        return redirect('diary:detail', slug=diary.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О заметке'
        return context


class DiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой записи.
    - После успешного создания, запись сохраняется за текущим пользователем.
    """
    model = Diary
    form_class = DiaryForm
    success_url = reverse_lazy('diary:list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.owner = self.request.user
        diary.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая заметка'
        context['title_h1'] = 'Создать заметку'
        return context


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления записи.
    - Пользователь может редактировать только свои записи.
    """
    model = Diary
    form_class = DiaryUpdateForm

    def get_queryset(self):
        return Diary.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('diary:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновить заметку'
        context['title_h1'] = 'Редактировать заметку'
        return context


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления записи.
    - Пользователь может удалить только свои записи.
    - После удаления происходит перенаправление на список записей.
    """
    model = Diary
    success_url = reverse_lazy('diary:list')

    def get_queryset(self):
        return Diary.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить заметку'
        return context


class DiaryModerationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Представление для модераторов.
    - Отображает список записей, которые находятся на модерации.
    - Пользователю должна быть выдана соответствующая роль для доступа к этой странице.
    """
    model = Diary
    template_name = 'diary/moderation_list.html'
    permission_required = 'diary.can_moderate'
    paginate_by = 10

    def get_queryset(self):
        return Diary.objects.filter(status='moderation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Модерация'
        return context


class DiaryModerationActionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Представление для модераторов.
    - Позволяет утвердить или отклонить запись, отправленную на модерацию.
    - При утверждении запись публикуется, при отклонении — отклоняется.
    """
    permission_required = 'diary.can_moderate'

    def post(self, request, *args, **kwargs):
        diary = get_object_or_404(Diary, slug=kwargs['slug'])

        if 'approve' in request.POST:
            diary.status = 'published'
            diary.is_published = True
            diary.save()
        elif 'reject' in request.POST:
            diary.status = 'rejected'
            diary.save()
        return HttpResponseRedirect(reverse('diary:moderation_list'))
