from django.db import models

from apps.customers.models import Customer
from config.mixins import TimestampMixin


class ProductProvider(models.TextChoices):
    # name = value, label
    KBINS = "kbins", "KB손해"
    KBLIFE = "kblife", "KB생명"
    NO_AFF = "no_aff", "소속없음"


class Product(TimestampMixin):
    name = models.CharField(max_length=200, null=False, blank=False)
    tag = models.CharField(max_length=100, null=True, blank=True)
    provider = models.CharField(
        max_length=10, null=False, choices=ProductProvider.choices
    )

    class Meta:
        db_table = "product"
        constraints = [
            models.UniqueConstraint(fields=["name", "tag"], name="product_name_tag")
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"[{self.provider}] {self.name}"
