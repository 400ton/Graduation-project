import secrets
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')  # Перенаправление на профиль пользователя или другую страницу
            else:
                messages.error(request, "Неверный email или пароль")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
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


def email_confirm(request, verification_code):
    user = get_object_or_404(User, verification_code=verification_code)
    if user:
        user.is_active = True
        user.verification_code = None
        user.save()
        return redirect('users:login')


class GeneratePasswordView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                password = User.objects.make_random_password(length=8)
                user.set_password(password)
                user.save()
                send_mail(
                    'Смена пароля',
                    f'Здравствуйте.Вы запросили генерацию нового пароля для локального сайта. '
                    f'Ваш новый пароль: {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return redirect(reverse("users:login"))
            except User.DoesNotExist:
                messages.error(self.request, "Такого пользователя не существует.")
                return redirect(reverse("users:reset_password"))
        else:
            messages.error(self.request, "Произошла ошибка при генерации пароля.")
            return super().form_invalid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
