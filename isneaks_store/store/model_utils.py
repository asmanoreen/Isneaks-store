from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """
    Base model that includes uuid and default created / updated timestamps.
    """
    standard_fields = ["id", "updated_at"]

    # created_at = models.DateTimeField(
    #     auto_now_add=True, db_index=True, verbose_name="created at"
    # )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name="updated at"
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        if self.id:
            return f"{self.id}"
        return "---"


class Auditable(models.Model):
    """
    Adds audiable attributes in model
    """
    standard_fields = ["updated_by"]

    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     null=True,
    #     blank=True,
    #     related_name="created%(app_label)s_%(class)s_related",
    #     on_delete=models.SET_NULL,
    # )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="updated%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
