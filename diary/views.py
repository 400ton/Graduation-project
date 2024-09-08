from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView, DetailView

from diary.models import Diary


class HomeListView(ListView):
    model = Diary
    template_name = "diary/home.html"
    queryset = Diary.objects.filter(is_published=False)  # выбираем только опубликованные записи
    paginate_by = 6  # опционально: добавляет пагинацию, например, по 6 записей на страницу

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный дневник'
        return context


class DiaryListView(ListView):
    model = Diary
    template_name = 'diary/diary_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список заметок'
        return context

    # def get_queryset(self):
    #     return get_cached_data(self.model)


class DiaryDetailView(DetailView):
    model = Diary
    template_name = 'diary/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О заметке'
        return context


class DiaryCreateView(CreateView):
    model = Diary
    fields = ('title', 'content', 'preview', )
    success_url = reverse_lazy('diary:list')

    def form_valid(self, form):
        diary = form.save()
        user = self.request.user
        diary.owner = user
        diary.save()
        if form.is_valid():
            new_entry = form.save()
            new_entry.slug = slugify(new_entry.title)
            new_entry.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать заметку'
        return context


class DiaryUpdateView(UpdateView):
    model = Diary
    fields = ('title', 'content', 'preview',)

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:list', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновить запись'
        return context


class DiaryDeleteView(DeleteView):
    model = Diary
    # success_url = reverse_lazy('diary:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить заметку'
        return context
