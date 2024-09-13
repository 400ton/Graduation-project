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
from pytils.translit import slugify


class HomeListView(ListView):
    model = Diary
    template_name = "diary/home.html"
    queryset = Diary.objects.filter(is_published=True)  # выбираем только опубликованные записи
    paginate_by = 5  # опционально: добавляет пагинацию, например, по 6 записей на страницу

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный дневник'
        return context


class DiaryListView(LoginRequiredMixin, ListView):
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
    model = Diary
    template_name = 'diary/diary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О заметке'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'publish' in request.POST:
            self.object.status = 'moderation'  # Изменение статуса на "На модерации"
            self.object.save()
            # Логика отправки уведомления модератору может быть здесь
        return redirect('diary:detail', slug=self.object.slug)

    @staticmethod
    def send_notification():
        send_mail(
            subject='Уведомление',
            message='Ваша запись достигла 100 просмотров!',
            from_email=EMAIL_HOST_USER,
            recipient_list=[User.email, ]
        )

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        Diary.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
        self.object.refresh_from_db()
        if self.object.views >= 100:
            self.send_notification()
        return self.object


class DiaryCreateView(LoginRequiredMixin, CreateView):
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
    model = Diary
    success_url = reverse_lazy('diary:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить заметку'
        return context


class DiaryModerationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/moderation_list.html'
    context_object_name = 'diaries'
    permission_required = 'diary.can_moderate_records'

    def get_queryset(self):
        # Возвращаем записи, которые находятся на модерации
        return Diary.objects.filter(status='moderation')


class DiaryModerationActionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'diary.can_moderate_records'

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
