from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.edit import FormView

User = get_user_model()

from .forms import (
    RegisterForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm,
)
from .mock_data import (
    TRANSLATIONS,
    DASHBOARD_STATS,
    INVOICES_RECORDS,
    LICENSES_SUMMARY,
    LICENSES_ITEMS,
    MACHINES_METRICS,
    MACHINES_LIST,
)


def get_language(request):
    lang = request.GET.get("lang", "pt")
    return lang if lang in TRANSLATIONS else "pt"


def get_toggle_url(request, lang):
    target = "pt" if lang == "en" else "en"
    return f"{request.path}?lang={target}"


def get_base_context(request, active_page):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    html_lang = "pt-BR" if lang == "pt" else "en"
    return {
        "active_page": active_page,
        "lang": lang,
        "html_lang": html_lang,
        "t": t,
        "toggle_lang_url": get_toggle_url(request, lang),
    }


class CustomLoginView(LoginView):
    template_name = "ledger/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request, active_page="login"))
        context["hide_navigation"] = True
        return context


class RegisterView(FormView):
    template_name = "ledger/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("ledger:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request, active_page="register"))
        context["hide_navigation"] = True
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        messages.success(
            self.request,
            "Cadastro realizado com sucesso! Agora você pode fazer login."
        )
        return redirect(self.success_url)


@login_required(login_url=reverse_lazy("ledger:login"))
def dashboard(request):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    context = get_base_context(request, "dashboard")
    context.update(
        {
            "page_title": t["dashboard_title"],
            "page_subtitle": t["dashboard_subtitle"],
            "btn_generate_report": t["btn_generate_report"],
            "btn_export_csv": t["btn_export_csv"],
            "stats": [
                {"label": t[stat["label"]], "value": stat["value"], "change": stat["change"], "icon": stat["icon"]}
                for stat in DASHBOARD_STATS
            ],
            "section_critical_alerts": t["section_critical_alerts"],
            "section_software_utilization": t["section_software_utilization"],
            "section_recent_history": t["section_recent_history"],
            "view_all": t["view_all"],
            "alerts": t["alerts"],
            "history": t["history"],
            "portfolios": t["portfolios"],
        }
    )
    return render(request, "ledger/dashboard.html", context)


def password_reset_request(request):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(
            reverse_lazy("ledger:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        )
        subject = "Ledger - Redefinição de senha"
        message = (
            f"Olá {user.first_name or user.username},\n\n"
            f"Para criar uma nova senha, acesse o link abaixo:\n{reset_url}\n\n"
            "Se você não solicitou a redefinição, ignore esta mensagem.\n"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        messages.success(request, "Link de redefinição enviado por e-mail.")
        return redirect("ledger:login")

    context = get_base_context(request, "login")
    context.update(
        {
            "page_title": t["reset_password_title"],
            "page_subtitle": t["reset_password_subtitle"],
            "reset_password_email_label": t["reset_password_email_label"],
            "reset_password_button": t["reset_password_button"],
            "reset_password_back_login": t["reset_password_back_login"],
            "form": form,
        }
    )
    context["hide_navigation"] = True
    return render(request, "ledger/password_reset.html", context)


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, "Link inválido ou expirado. Solicite uma nova redefinição.")
        return redirect("ledger:password_reset")

    lang = get_language(request)
    t = TRANSLATIONS[lang]
    form = PasswordResetConfirmForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user.set_password(form.cleaned_data["password1"])
        user.save()
        messages.success(request, "Senha redefinida com sucesso. Agora faça login.")
        return redirect("ledger:login")

    context = get_base_context(request, "login")
    context.update(
        {
            "page_title": t["new_password_title"],
            "page_subtitle": t["new_password_subtitle"],
            "new_password_label": t["new_password_label"],
            "new_password_confirm_label": t["new_password_confirm_label"],
            "new_password_button": t["new_password_button"],
            "reset_password_back_login": t["reset_password_back_login"],
            "form": form,
        }
    )
    context["hide_navigation"] = True
    return render(request, "ledger/password_reset_confirm.html", context)


@login_required(login_url=reverse_lazy("ledger:login"))
def profile(request):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    context = get_base_context(request, "profile")
    context.update(
        {
            "page_title": t["profile_title"],
            "page_subtitle": t["profile_subtitle"],
            "label_username": t["label_username"],
            "label_name": t["label_name"],
            "label_email": t["label_email"],
            "label_date_joined": t["label_date_joined"],
            "profile_user": request.user,
        }
    )
    return render(request, "ledger/profile.html", context)


@login_required(login_url=reverse_lazy("ledger:login"))
def invoices(request):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    context = get_base_context(request, "invoices")
    context.update(
        {
            "page_title": t["page_invoices"],
            "page_subtitle": t["invoices_description"],
            "btn_new_invoice": t["btn_new_invoice"],
            "label_nf_number": t["label_nf_number"],
            "label_supplier": t["label_supplier"],
            "label_date": t["label_date"],
            "label_value": t["label_value"],
            "label_files": t["label_files"],
            "form_manual_entry": t["form_manual_entry"],
            "form_manual_entry_description": t["form_manual_entry_description"],
            "form_nf_number": t["form_nf_number"],
            "form_series": t["form_series"],
            "form_supplier": t["form_supplier"],
            "form_cnpj": t["form_cnpj"],
            "form_date": t["form_date"],
            "form_total_value": t["form_total_value"],
            "form_drop_label": t["form_drop_label"],
            "form_drop_note": t["form_drop_note"],
            "btn_finalize_record": t["btn_finalize_record"],
            "modal_series_label": t["modal_series_label"],
            "label_monthly_cap": t["label_monthly_cap"],
            "label_validated": t["label_validated"],
            "records": INVOICES_RECORDS,
        }
    )
    return render(request, "ledger/invoices.html", context)


@login_required(login_url=reverse_lazy("ledger:login"))
def licenses(request):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    context = get_base_context(request, "licenses")
    context.update(
        {
            "page_title": t["page_licenses"],
            "page_subtitle": t["licenses_description"],
            "search_placeholder": t["search_licenses"],
            "btn_filters": t["btn_filters"],
            "summary": [
                {"title": t[summary["title"]], "value": summary["value"], "accent": summary["accent"]}
                for summary in LICENSES_SUMMARY
            ],
            "items": [
                {
                    "name": item["name"],
                    "type": t["label_license_type"],
                    "usage": item["usage"],
                    "expires": item["expires"],
                    "status": item["status"]
                }
                for item in LICENSES_ITEMS
            ],
            "label_software_asset": t["label_software_asset"],
            "label_allocation": t["label_allocation"],
            "label_expiration": t["label_expiration"],
            "label_status": t["label_status"],
            "label_license_key": t["label_license_key"],
            "label_purchase_reference": t["label_purchase_reference"],
            "label_asset_owner": t["label_asset_owner"],
            "label_audit_interval": t["label_audit_interval"],
            "label_lifecycle_actions": t["label_lifecycle_actions"],
            "btn_renew_license": t["btn_renew_license"],
            "btn_export_compliance": t["btn_export_compliance"],
            "btn_revoke_access": t["btn_revoke_access"],
        }
    )
    return render(request, "ledger/licenses.html", context)


@login_required(login_url=reverse_lazy("ledger:login"))
def machines(request):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    context = get_base_context(request, "machines")
    context.update(
        {
            "page_title": t["page_machines"],
            "metrics": [
                {"label": t[metric["label"]], "value": metric["value"]}
                for metric in MACHINES_METRICS
            ],
            "table_workstation_identity": t["table_workstation_identity"],
            "table_current_user": t["table_current_user"],
            "table_department": t["table_department"],
            "table_status": t["table_status"],
            "software_installed": t["software_installed"],
            "linked_licenses": t["linked_licenses"],
            "license_id": t["license_id"],
            "renewal_date": t["renewal_date"],
            "machines": MACHINES_LIST,
        }
    )
    return render(request, "ledger/machines.html", context)
