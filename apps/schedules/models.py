from django.db import models

from apps.customers.models import Customer
from apps.users.models import User
from config.mixins import TimestampMixin


class CustomerSchedule(TimestampMixin):
    customer = models.ForeignKey(
        Customer, null=False, related_name="schedules", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, null=False)
    date = models.DateField(null=False)
    has_end_time = models.BooleanField(default=False)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    fc = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "customer_schedule"

    def __str__(self):
        return f"[{self.id}] {self.title}"

    def __repr__(self):
        return f"[{self.customer} {self.title}"
