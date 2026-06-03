from decimal import Decimal
from datetime import datetime

from django.db import migrations


def parse_date(value):
    try:
        return datetime.strptime(value, "%b %d, %Y").date()
    except ValueError:
        return None


def parse_amount(value):
    cleaned = value.replace("$", "").replace(",", "").strip()
    return Decimal(cleaned)


def load_mock_data(apps, schema_editor):
    InvoiceRecord = apps.get_model("ledger", "InvoiceRecord")
    LicenseItem = apps.get_model("ledger", "LicenseItem")
    Machine = apps.get_model("ledger", "Machine")

    from ledger.mock_data import INVOICES_RECORDS, LICENSES_ITEMS, MACHINES_LIST

    for record in INVOICES_RECORDS:
        InvoiceRecord.objects.create(
            number=record["number"],
            supplier=record["supplier"],
            date=parse_date(record["date"]),
            value=parse_amount(record["value"]),
            currency="BRL",
        )

    for item in LICENSES_ITEMS:
        expires = parse_date(item["expires"]) if item.get("expires") else None
        LicenseItem.objects.create(
            name=item["name"],
            license_type=item["type"],
            usage=item["usage"],
            expires=expires,
            status=item["status"],
        )

    for machine in MACHINES_LIST:
        Machine.objects.create(
            workstation_id=machine["id"],
            model=machine["model"],
            user=machine["user"],
            department=machine["department"],
            status=machine["status"],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("ledger", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_mock_data),
    ]
