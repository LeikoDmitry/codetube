from django.urls import path
from .views import action

app_name = 'tube'
urlpatterns = [
    path('', action.Auth.index_action, name='index'),
    path('login', action.Auth.login_action, name='login'),
    path('register', action.Auth.register_action, name='register'),
    path('reset', action.Auth.reset_action, name='reset'),
    path('email', action.Auth.email_action, name='email')
]