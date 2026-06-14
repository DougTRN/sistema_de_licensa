from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from . import views

app_name = "ledger"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("ledger:login")), name="logout"),

    path("password_reset/", PasswordResetView.as_view(
        template_name="ledger/password_reset.html",
        email_template_name="ledger/activation_email.txt",
        success_url=reverse_lazy("ledger:password_reset_done")
    ), name="password_reset"),
    path("password_reset_done/", PasswordResetDoneView.as_view(
        template_name="ledger/password_reset.html"
    ), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="ledger/password_reset_confirm.html",
        success_url=reverse_lazy("ledger:password_reset_complete")
    ), name="password_reset_confirm"),
    path("password_reset_complete/", PasswordResetCompleteView.as_view(
        template_name="ledger/password_reset_confirm.html"
    ), name="password_reset_complete"),

    path("profile/", views.profile, name="profile"),
    path("", views.dashboard, name="dashboard"),
    path("invoices/", views.invoices, name="invoices"),
    path("invoices/save/", views.save_invoice, name="save_invoice"),
    path("licenses/", views.licenses, name="licenses"),
    path("machines/", views.machines, name="machines"),
]
