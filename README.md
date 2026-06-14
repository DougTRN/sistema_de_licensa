# Architectural Ledger Django Prototype

Uma aplicação Django simples com templates que reproduzem o design das páginas fornecidas.

## Instalação

1. Crie e ative um virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. O projeto já roda com SQLite por padrão usando `db.sqlite3`.

4. Se quiser usar PostgreSQL em vez de SQLite, defina também `USE_POSTGRES=1` e as variáveis abaixo. O `.env` do projeto já pode conter essas configurações:

```powershell
USE_POSTGRES=1
POSTGRES_DB=architectural_ledger
POSTGRES_USER=postgres
POSTGRES_PASSWORD=(SUA SENHA DO BANCO)
POSTGRES_HOST=localhost
POSTGRES_PORT=(PORTA DO BANCO)
```

5. Rode as migrações e inicie o servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

6. Configurar e-mail real

- Crie um arquivo `.env` na raiz do projeto usando `.env.example` como modelo.
- No ambiente local, você pode usar SMTP real para enviar o e-mail de ativação.

Exemplo de variáveis:

```powershell
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@dominio.com
EMAIL_HOST_PASSWORD=sua-senha-ou-app-password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL="Ledger <noreply@ledger.local>"
```

Se usar Gmail, ative o App Password e use a senha de app.

7. Acesse no navegador:

- `http://127.0.0.1:8000/` - Dashboard
- `http://127.0.0.1:8000/invoices/` - Invoices
- `http://127.0.0.1:8000/licenses/` - Licenses
- `http://127.0.0.1:8000/machines/` - Machines
