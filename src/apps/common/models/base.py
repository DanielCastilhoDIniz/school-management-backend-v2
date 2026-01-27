from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Base(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("UUID"),
        help_text=_("Universally unique identifier")
        )

    # TIMESTAMPS (Data/Hora)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Date and time when the record was created")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Date and time when the record was last updated")
    )

    # Opcional:
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Deleted At"),
        help_text=_("Date and time when the record was soft deleted")
    )

    # METADADOS E METRICS
    # Melhor nome para evitar conflitos
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this record is active")
    )

    # Para versionamento/controle de publicação
    is_published = models.BooleanField(
        default=False,
        verbose_name=_("Is Published"),
        help_text=_("Whether this record is published publicly")
    )

    # Para controle de versões/draft
    version = models.PositiveIntegerField(
        default=1,
        editable=False,
        verbose_name=_("Version"),
        help_text=_("Record version number")
    )

    # Para ordenação personalizada
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sort Order"),
        help_text=_("Custom sorting order (lower numbers appear first)")
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']  # Duplo critério
        get_latest_by = 'updated_at'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_published']),
            models.Index(fields=['uuid']),
        ]

        def __str__(self):
            return f"{self.__class__.__name__} #{
                self.pk or 'unsaved'}"
