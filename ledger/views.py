from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import RegisterForm

User = get_user_model()


TRANSLATIONS = {
    "en": {
        "nav_dashboard": "Dashboard",
        "nav_invoices": "Invoices",
        "nav_licenses": "Licenses",
        "nav_machines": "Machines",
        "btn_new_asset": "New Asset",
        "btn_settings": "Settings",
        "btn_support": "Support",
        "search_placeholder": "Search...",
        "lang_toggle": "Português",
        "dashboard_title": "Strategic Overview",
        "dashboard_subtitle": "Global IT inventory and license compliance status.",
        "btn_generate_report": "Generate Report",
        "btn_export_csv": "Export CSV",
        "card_total_assets": "Total Assets",
        "card_active_licenses": "Active Licenses",
        "card_monthly_spend": "Monthly Spend",
        "section_critical_alerts": "Critical Alerts",
        "section_software_utilization": "Software Utilization by Sector",
        "section_recent_history": "Recent Movement History",
        "view_all": "View all",
        "alerts": [
            {
                "title": "License Compliance Risk",
                "description": "Adobe Creative Cloud licenses exceeded. 142 machines detected vs 120 allocated seats. Potential audit liability: $3,200.",
                "label": "2 issues detected",
                "type": "critical",
            },
            {
                "title": "Expiring Software Contracts",
                "description": "JetBrains Enterprise renewal due in 14 days. Estimated cost: $12,450.",
                "label": "Review Invoice",
                "type": "warning",
            },
        ],
        "history": [
            {"title": "MacBook Pro M3 Provisioned", "subtitle": "Assigned to: Sara Chen (Engineering)", "tag": "ASSET TAG AM-4320", "time": "14 mins ago", "type": "success"},
            {"title": "License Reallocation", "subtitle": "AutoCAD Suite moved from Marketing to R&D pool.", "tag": "SOFT-ASSET", "time": "1 hour ago", "type": "info"},
            {"title": "Decommissioned Hardware", "subtitle": "Dell XPS 15 (2020) retired for parts.", "tag": "END-OF-LIFE", "time": "4 hours ago", "type": "danger"},
        ],
        "portfolios": [
            {"name": "Microsoft 365 Enterprise", "description": "Standard Enterprise Suite", "value": "1,200 seats allocated", "accent": "dark"},
            {"name": "Slack Business+", "description": "Messaging & Collab", "value": "840", "accent": "green"},
            {"name": "Adobe Creative Cloud", "description": "Creative Suite", "value": "142", "accent": "red"},
        ],
        "page_invoices": "Invoices",
        "invoices_description": "Digital curation of fiscal assets and expenditure verification.",
        "btn_new_invoice": "New Invoice",
        "label_nf_number": "NF Number",
        "label_supplier": "Supplier",
        "label_date": "Date",
        "label_value": "Value",
        "label_files": "Files",
        "form_manual_entry": "Manual Entry",
        "form_manual_entry_description": "Enter fiscal data precisely as issued.",
        "form_nf_number": "NF Number",
        "form_supplier": "Supplier",
        "form_date": "Date",
        "form_total_value": "Total Value",
        "form_drop_label": "Drop PDF or XML here",
        "form_drop_note": "Maximum file size: 10MB",
        "btn_finalize_record": "Finalize Record",
        "label_monthly_cap": "Monthly Cap",
        "label_validated": "Validated",
        "page_licenses": "Software License Inventory",
        "licenses_description": "Software license control and strategic compliance.",
        "search_licenses": "Search licenses...",
        "btn_filters": "Filters",
        "label_expiring_next_30_days": "Expiring Next 30 Days",
        "label_healthy_status": "Healthy Status",
        "label_software_asset": "Software Asset",
        "label_license_type": "License Type",
        "label_allocation": "Allocation",
        "label_expiration": "Expiration",
        "label_status": "Status",
        "label_license_key": "License Key / Secret",
        "label_purchase_reference": "Purchase Reference",
        "label_asset_owner": "Asset Owner",
        "label_audit_interval": "Audit Interval",
        "label_lifecycle_actions": "Lifecycle Actions",
        "btn_renew_license": "Renew License",
        "btn_export_compliance": "Export Compliance PDF",
        "btn_revoke_access": "Revoke Access",
        "page_machines": "Machines Control",
        "metric_total_assets": "Total Assets",
        "metric_active_now": "Active Now",
        "metric_avg_health": "Avg. Health",
        "table_workstation_identity": "Workstation Identity",
        "table_current_user": "Current User",
        "table_department": "Department",
        "table_status": "Status",
        "software_installed": "Installed Software",
        "linked_licenses": "Linked Licenses",
        "license_id": "License ID",
        "renewal_date": "Renewal",
    },
    "pt": {
        "nav_dashboard": "Painel",
        "nav_invoices": "Notas Fiscais",
        "nav_licenses": "Licenças",
        "nav_machines": "Máquinas",
        "btn_new_asset": "Novo Ativo",
        "btn_settings": "Configurações",
        "btn_support": "Suporte",
        "search_placeholder": "Pesquisar...",
        "lang_toggle": "English",
        "dashboard_title": "Visão Estratégica",
        "dashboard_subtitle": "Inventário global de TI e status de conformidade.",
        "btn_generate_report": "Gerar Relatório",
        "btn_export_csv": "Exportar CSV",
        "card_total_assets": "Total de Ativos",
        "card_active_licenses": "Licenças Ativas",
        "card_monthly_spend": "Gasto Mensal",
        "section_critical_alerts": "Alertas Críticos",
        "section_software_utilization": "Utilização de Software por Setor",
        "section_recent_history": "Histórico de Movimentações",
        "view_all": "Ver tudo",
        "alerts": [
            {
                "title": "Risco de Conformidade de Licença",
                "description": "Licenças do Adobe Creative Cloud excedidas. 142 máquinas detectadas vs 120 assentos alocados. Possível passivo de auditoria: $3.200.",
                "label": "2 problemas detectados",
                "type": "critical",
            },
            {
                "title": "Contratos de Software a Vencer",
                "description": "Renovação do JetBrains Enterprise em 14 dias. Custo estimado: $12.450.",
                "label": "Revisar Nota",
                "type": "warning",
            },
        ],
        "history": [
            {"title": "MacBook Pro M3 Provisionado", "subtitle": "Atribuído para: Sara Chen (Engenharia)", "tag": "TAG DO ATIVO AM-4320", "time": "14 min atrás", "type": "success"},
            {"title": "Realocação de Licença", "subtitle": "Suite AutoCAD movida de Marketing para o pool de P&D.", "tag": "SOFT-ATIVO", "time": "1 hora atrás", "type": "info"},
            {"title": "Hardware Descomissionado", "subtitle": "Dell XPS 15 (2020) aposentado para peças.", "tag": "FIM-DE-VIDA", "time": "4 horas atrás", "type": "danger"},
        ],
        "portfolios": [
            {"name": "Microsoft 365 Enterprise", "description": "Suite Empresarial Padrão", "value": "1.200 assentos alocados", "accent": "dark"},
            {"name": "Slack Business+", "description": "Mensagens e Colaboração", "value": "840", "accent": "green"},
            {"name": "Adobe Creative Cloud", "description": "Suite Criativa", "value": "142", "accent": "red"},
        ],
        "page_invoices": "Notas Fiscais",
        "invoices_description": "Curadoria digital de ativos fiscais e verificação de despesas.",
        "btn_new_invoice": "Nova Nota",
        "label_nf_number": "Número NF",
        "label_supplier": "Fornecedor",
        "label_date": "Data",
        "label_value": "Valor",
        "label_files": "Arquivos",
        "form_manual_entry": "Entrada Manual",
        "form_manual_entry_description": "Insira os dados fiscais com precisão conforme emitido.",
        "form_nf_number": "Número NF",
        "form_supplier": "Fornecedor",
        "form_date": "Data",
        "form_total_value": "Valor Total",
        "form_drop_label": "Solte PDF ou XML aqui",
        "form_drop_note": "Tamanho máximo do arquivo: 10MB",
        "btn_finalize_record": "Finalizar Registro",
        "label_monthly_cap": "Cap Mensal",
        "label_validated": "Validado",
        "page_licenses": "Inventário de Licenças de Software",
        "licenses_description": "Controle de Licenças e Conformidade Estratégica",
        "search_licenses": "Pesquisar licenças...",
        "btn_filters": "Filtros",
        "label_expiring_next_30_days": "Vencendo nos Próximos 30 Dias",
        "label_healthy_status": "Status Saudável",
        "label_software_asset": "Ativo de Software",
        "label_license_type": "Tipo de Licença",
        "label_allocation": "Alocação",
        "label_expiration": "Expiração",
        "label_status": "Status",
        "label_license_key": "Chave / Segredo da Licença",
        "label_purchase_reference": "Referência de Compra",
        "label_asset_owner": "Responsável pelo Ativo",
        "label_audit_interval": "Intervalo de Auditoria",
        "label_lifecycle_actions": "Ações de Ciclo de Vida",
        "btn_renew_license": "Renovar Licença",
        "btn_export_compliance": "Exportar PDF de Conformidade",
        "btn_revoke_access": "Revogar Acesso",
        "page_machines": "Controle de Máquinas",
        "metric_total_assets": "Total de Ativos",
        "metric_active_now": "Ativas Agora",
        "metric_avg_health": "Média de Saúde",
        "table_workstation_identity": "Identidade da Estação",
        "table_current_user": "Usuário Atual",
        "table_department": "Departamento",
        "table_status": "Status",
        "software_installed": "Software Instalado",
        "linked_licenses": "Licenças Vinculadas",
        "license_id": "ID da Licença",
        "renewal_date": "Renovação",
    },
}


def get_language(request):
    lang = request.GET.get("lang", "en")
    return lang if lang in TRANSLATIONS else "en"


def get_toggle_url(request, lang):
    target = "pt" if lang == "en" else "en"
    return f"{request.path}?lang={target}"


def get_base_context(request, active_page):
    lang = get_language(request)
    t = TRANSLATIONS[lang]
    return {
        "active_page": active_page,
        "lang": lang,
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
                {"label": t["card_total_assets"], "value": "1,520", "change": "+8%", "icon": "inventory_2"},
                {"label": t["card_active_licenses"], "value": "932", "change": "+5%", "icon": "verified"},
                {"label": t["card_monthly_spend"], "value": "$48,300", "change": "-2%", "icon": "paid"},
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
            "form_supplier": t["form_supplier"],
            "form_date": t["form_date"],
            "form_total_value": t["form_total_value"],
            "form_drop_label": t["form_drop_label"],
            "form_drop_note": t["form_drop_note"],
            "btn_finalize_record": t["btn_finalize_record"],
            "label_monthly_cap": t["label_monthly_cap"],
            "label_validated": t["label_validated"],
            "records": [
                {"number": "#NF-902341", "supplier": "DataStream Systems", "date": "Oct 12, 2024", "value": "$12,450.00"},
                {"number": "#NF-882109", "supplier": "CloudScale Infra", "date": "Oct 08, 2024", "value": "$4,820.50"},
                {"number": "#NF-876551", "supplier": "Vertex Security", "date": "Sep 28, 2024", "value": "$2,100.00"},
                {"number": "#NF-854123", "supplier": "Core Net Tech", "date": "Sep 15, 2024", "value": "$18,900.00"},
            ],
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
                {"title": t["card_total_assets"], "value": "482", "accent": "primary"},
                {"title": t["label_healthy_status"], "value": "94%", "accent": "secondary"},
                {"title": t["label_expiring_next_30_days"], "value": "12 Licenses", "accent": "dark"},
            ],
            "items": [
                {"name": "Windows 11 Enterprise", "type": t["label_license_type"], "usage": "215 / 250", "expires": "Oct 14, 2025", "status": "ACTIVE"},
                {"name": "Office 365 Business Premium", "type": t["label_license_type"], "usage": "105 / 100", "expires": "Nov 22, 2024", "status": "OVER-LIMIT"},
                {"name": "Adobe Creative Cloud", "type": t["label_license_type"], "usage": "12 / 15", "expires": "Dec 01, 2023", "status": "EXPIRED"},
                {"name": "Slack Enterprise Grid", "type": t["label_license_type"], "usage": "450 / 500", "expires": "May 10, 2025", "status": "ACTIVE"},
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
                {"label": t["metric_total_assets"], "value": "128"},
                {"label": t["metric_active_now"], "value": "94"},
                {"label": t["metric_avg_health"], "value": "98%"},
            ],
            "table_workstation_identity": t["table_workstation_identity"],
            "table_current_user": t["table_current_user"],
            "table_department": t["table_department"],
            "table_status": t["table_status"],
            "software_installed": t["software_installed"],
            "linked_licenses": t["linked_licenses"],
            "license_id": t["license_id"],
            "renewal_date": t["renewal_date"],
            "machines": [
                {"id": "WS-PRD-4029", "model": "Dell Precision 5820", "user": "Elena Rodriguez", "department": "Engineering", "status": "active"},
                {"id": "MBP-DSG-011", "model": "MacBook Pro M2", "user": "Marcus Thorne", "department": "Design", "status": "active"},
                {"id": "WS-FIN-992", "model": "HP Z6 G4 Tower", "user": "Sarah Jenkins", "department": "Finance", "status": "offline"},
                {"id": "WS-PRD-102", "model": "Dell Latitude 7420", "user": "Arthur Dent", "department": "Operations", "status": "active"},
                {"id": "MBP-EXE-001", "model": "MacBook Pro 16'", "user": "Thomas Shelby", "department": "Executive", "status": "active"},
            ],
        }
    )
    return render(request, "ledger/machines.html", context)
