from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    first_name = forms.CharField(required=True, label="Nome")

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_password2(self):
        password2 = super().clean_password2()
        password1 = self.cleaned_data.get("password1")
        if password1 and password2:
            if len(password2) < 8:
                raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r"[A-Z]", password2):
                raise forms.ValidationError("A senha deve incluir pelo menos uma letra maiúscula.")
            if not re.search(r"\d", password2):
                raise forms.ValidationError("A senha deve incluir pelo menos um número.")
        return password2
