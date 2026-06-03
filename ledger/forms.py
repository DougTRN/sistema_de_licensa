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


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, label="E-mail")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Nenhuma conta encontrada para este e-mail.")
        return email

    def get_user(self):
        email = self.cleaned_data.get("email")
        return User.objects.filter(email__iexact=email).first()


class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        label="Senha",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        required=True,
        label="Confirmar senha",
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        if password1:
            if len(password1) < 8:
                raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r"[A-Z]", password1):
                raise forms.ValidationError("A senha deve incluir pelo menos uma letra maiúscula.")
            if not re.search(r"\d", password1):
                raise forms.ValidationError("A senha deve incluir pelo menos um número.")
        return cleaned_data
