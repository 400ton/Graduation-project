from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from config.settings import EMAIL_HOST_USER
from diary.forms import DiaryForm, DiaryUpdateForm
from diary.models import Diary
from users.models import User


class HomeListView(ListView):
    """
    Представление для отображения главной страницы с опубликованными записями.
    - queryset: выбираются только записи со статусом is_published=True.
    """
    model = Diary
    template_name = "diary/home.html"
    queryset = Diary.objects.filter(is_published=True)  # выбираем только опубликованные записи
    paginate_by = 5  # опционально: добавляет пагинацию, например, по 6 записей на страницу

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список заметок'
        return context

    def get_queryset(self):
        return Diary.objects.filter(owner=self.request.user)


class DiaryDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей записи.
    - При каждом просмотре запись увеличивает счетчик просмотров.
    - Если просмотров более 100, отправляется уведомление.
    - При POST запросе запись может быть отправлена на модерацию.
    """
    model = Diary
    template_name = 'diary/diary_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        Diary.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
        self.object.refresh_from_db()
        if self.object.views >= 100:
            send_mail(
                subject='Уведомление',
                message='Ваша запись достигла 100 просмотров!',
                from_email=EMAIL_HOST_USER,
                recipient_list=[self.object.owner.email,]
            )
        return self.object

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'publish' in request.POST:
            self.object.status = 'moderation'  # Изменение статуса на "На модерации"
            self.object.save()
        return redirect('diary:detail', slug=self.object.slug)

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
        context['title'] = 'Новая запись'
        return context


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления записи.
    - Пользователь может редактировать только свои записи.
    """
    model = Diary
    form_class = DiaryUpdateForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновить запись'
        return context


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления записи.
    - Пользователь может удалить только свои записи.
    - После удаления происходит перенаправление на список записей.
    """
    model = Diary
    success_url = reverse_lazy('diary:list')

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
