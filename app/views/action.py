from django.shortcuts import render


class Auth:

    @staticmethod
    def index_action(request):
        return render(request, 'app/index.html')

    @staticmethod
    def login_action(request):
        return render(request, 'app/login.html')

    @staticmethod
    def register_action(request):
        return render(request, 'app/register.html')

    @staticmethod
    def reset_action(request):
        return render(request, 'app/reset.html')

    @staticmethod
    def email_action(request):
        return render(request, 'app/email.html')


class Channel:
    pass
