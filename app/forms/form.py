from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirmation")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
