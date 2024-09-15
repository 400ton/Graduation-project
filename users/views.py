import secrets
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm, CustomPasswordResetForm
from users.models import User


def login_view(request):
    """
    Представление для входа пользователя.
    Проверяет введенные данные, аутентифицирует пользователя с использованием email и пароля.
    При успешной аутентификации перенаправляет на страницу с записями (diary:list).
    """

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('diary:list')
    return render(request, 'users/login.html', {'form': form, 'title': 'Войти в аккаунт'})


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    Сохраняет пользователя в неактивном состоянии и отправляет email для подтверждения.
    После успешной регистрации перенаправляет на страницу входа.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Обрабатывает сохранение формы. Создает неактивного пользователя с кодом подтверждения.
        Отправляет email с подтверждением.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password1'])
        verification_code = secrets.token_hex(16)
        user.verification_code = verification_code
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{verification_code}'

        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


def email_confirm(request, verification_code):
    """
    Проверка кода верификации, активирует профиль пользователя
    """
    user = get_object_or_404(User, verification_code=verification_code)
    if user.is_active:
        messages.info(request, 'Аккаунт уже активирован.')
    else:
        user.is_active = True
        user.verification_code = None
        user.save()
        return redirect('users:login')


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения профиля пользователя.
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, **kwargs):
        return self.request.user


class GeneratePasswordView(PasswordResetView):
    """
    Представление для генерации нового пароля.
    Генерирует новый пароль и отправляет его на email пользователя
    """
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/reset_password.html'

    def form_valid(self, form):
        """
        Обрабатывает форму. Генерирует новый пароль для пользователя и отправляет его на email.
        """
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            password = User.objects.make_random_password(length=8)
            user.set_password(password)
            user.save()

            send_mail(
                'Смена пароля',
                f'Здравствуйте. Вы запросили генерацию нового пароля для локального сайта. '
                f'Ваш новый пароль: {password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except User.DoesNotExist:
            messages.error(self.request, "Пользователь с таким email не найден.")
            return super().form_invalid(form)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Восстановление пароля'
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления профиля пользователя.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context
