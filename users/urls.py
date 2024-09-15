from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, UserProfileUpdateView, email_confirm, GeneratePasswordView, login_view, \
    UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:verification_code>/', email_confirm, name='email-confirm'),
    path('reset/', GeneratePasswordView.as_view(), name='reset'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
