from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
