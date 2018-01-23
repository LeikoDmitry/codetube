from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
                return redirect('tube:login')

    @staticmethod
    def reset_action(request):
        return render(request, 'app/reset.html')

    @staticmethod
    def email_action(request):
        return render(request, 'app/email.html')

    @staticmethod
    def logout_action(request):
        logout(request)
        return redirect('tube:login')


class Channel:
    """Channel classes actions"""
    pass
