from django.db import models


class InvoiceRecord(models.Model):
    number = models.CharField(max_length=50)
    supplier = models.CharField(max_length=255)
    date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="BRL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Invoice Record"
        verbose_name_plural = "Invoice Records"

    def __str__(self):
        return self.number


class LicenseItem(models.Model):
    name = models.CharField(max_length=255)
    license_type = models.CharField(max_length=100)
    usage = models.CharField(max_length=50)
    expires = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "License Item"
        verbose_name_plural = "License Items"

    def __str__(self):
        return self.name


class Machine(models.Model):
    workstation_id = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __str__(self):
        return self.workstation_id
