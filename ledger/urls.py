from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from . import views

app_name = "ledger"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("ledger:login")), name="logout"),
    path("password-reset/", views.password_reset_request, name="password_reset"),
    path("password-reset/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("profile/", views.profile, name="profile"),
    path("", views.dashboard, name="dashboard"),
    path("invoices/", views.invoices, name="invoices"),
    path("licenses/", views.licenses, name="licenses"),
    path("machines/", views.machines, name="machines"),
]
