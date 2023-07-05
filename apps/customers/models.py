from django.db import models

from config.mixins import TimestampMixin


class Customer(TimestampMixin):
    class Calendar(models.TextChoices):
        LUNAR = "lunar", "음력"
        SOLAR = "solar", "양력"

    class EnticementStatus(models.TextChoices):
        PRE_PROGRESS = "pre-progress", "유치예정"
        IN_PROGRESS = "in-progress", "유치중"
        PROGRESS_COMPLETE = "progress-complete", "유치완료"

    class AttentionFlag(models.TextChoices):
        RED = "red", "red"
        ORANGE = "orange", "orange"
        YELLOW = "yellow", "yellow"

    name = models.CharField(max_length=10, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    calendar = models.CharField(
        max_length=5, null=False, choices=Calendar.choices, default=Calendar.SOLAR.value
    )
    enrollment_date = models.DateField(null=True, blank=False)
    enticement_status = models.CharField(
        max_length=20,
        null=False,
        choices=EnticementStatus.choices,
        default=EnticementStatus.IN_PROGRESS.value,
    )
    flag = models.CharField(max_length=10, null=True)
    fc = models.ForeignKey("users.User", on_delete=models.CASCADE, null=False)
    insurances = models.ManyToManyField("products.Product")

    class Meta:
        db_table = "customer"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "date_of_birth", "fc"], name="customer_fc"
            )
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"[{self.id}] {self.name}"


class CustomerNote(TimestampMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(max_length=4000, null=False, blank=True)

    class Meta:
        db_table = "customer_note"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"[{self.id}] {self.title}"
