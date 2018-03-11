from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password_confirmation = forms.CharField(max_length=255)
    channel_name =  forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirmation")
        if password != confirm_password:
            self.add_error('password', 'Password and confirm_password does not match')
        try:
            email = cleaned_data['email']
            User.objects.get(email=email)
            self.add_error('email', 'Email exists')
        except User.DoesNotExist:
            pass


class ResetForm(forms.Form):

    email = forms.EmailField(max_length=255)

    def clean(self):
        try:
            cleaned_data = super(ResetForm, self).clean()
            email = cleaned_data['email']
            User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error('email', 'Email not exists')




