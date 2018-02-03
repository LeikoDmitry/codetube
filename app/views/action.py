from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from app.forms.form import UserRegistrationForm


class Auth:
    """Auth classes action"""

    @staticmethod
    @login_required(login_url='/login')
    def index_action(request):
        return render(request, 'app/index.html')

    @staticmethod
    def login_action(request):
        if request.method != 'POST':
            return render(request, 'app/login.html')
        else:
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = User.objects.get(email=email)
                user_login = authenticate(request, username=user.username, password=password)
                if user_login is not None:
                    login(request, user_login)
                    return redirect('tube:index')
                else:
                    return redirect('tube:login')
            except User.DoesNotExist:
                return redirect('tube:login')

    @staticmethod
    def register_action(request):
        if request.method != 'POST':
            return render(request, 'app/register.html')
        else:
            form = UserRegistrationForm(request.POST)
            if not form.is_valid():
                return redirect('tube:register')
            else:
                name = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                user_created = User.objects.create_user(username=name, email=email, password=password)
                if user_created:
                    user_login = authenticate(request, username=name, password=password)
                    login(request, user_login)
                    return redirect('tube:index')

    @staticmethod
    def reset_action(request):
        return render(request, 'app/reset.html')

    @staticmethod
    def email_action(request):
        if request.method != 'POST':
            return render(request, 'app/email.html')
        else:
            try:
                email = request.POST['email']
                user_reset = User.objects.get(email=email)
                subject, from_email, to = 'Reset password', 'admin@codetube', user_reset.email
                url = 'http://localhost:8000' + '/reset?code=' + get_random_string(length=32)
                html_content = render_to_string('app/reset_mail.html', {
                    'email': user_reset.email,
                    'url': url,
                })
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('tube:login')
            except User.DoesNotExist:
                return render(request, 'app/email.html')

    @staticmethod
    def logout_action(request):
        logout(request)
        return redirect('tube:login')


class Channel:
    """Channel classes actions"""
    pass
