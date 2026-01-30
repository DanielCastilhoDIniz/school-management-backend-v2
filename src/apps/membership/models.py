from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from src.apps.common.models.base import Base

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


class Membership(Base):
    """
    Vínculo entre um usuário e um contexto institucional
    (Unidade, Rede, Turma), com papel, estado,
     período de validade e histórico de auditoria.
    """

    # num
    class Roles(models.TextChoices):
        STUDENT = 'student', _('Student')
        TEACHER = 'teacher', _('Teacher')
        MANAGER = 'manager', _('Manager')
        SECRETARY = 'secretary', _('Secretary')
        DIRECTOR = 'director', _('Network Director')
        PARENTS = 'parents', _('Parents')
        OTHER = 'other', _('Other')

    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        SUSPENDED = 'suspended', _('Suspended')
        COMPLETED = 'completed', _('Completed')

    # Main Fields
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    # Generic ForeignKey for Context (Unit, Network, Class)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
        )
    object_id = models.PositiveIntegerField()
    context = GenericForeignKey(
        'content_type',
        'object_id'
        )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices
        )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
        )

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    # Auditability
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    updated_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    # Validators
    def clean(self):
        super().clean()

        # Validation of the uniqueness of an active link
        # in the same context and role.
        if self.status == self.Status.ACTIVE:
            existing = Membership.objects.filter(
                user=self.user,
                content_type=self.content_type,
                object_id=self.object_id,
                role=self.role,
                status=self.Status.ACTIVE
            )
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(
                    f'User {self.user} already has an active {self.role} '
                    'membership in this context.'
                )

        # Date validation
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                _('End date cannot be earlier than start date.'))

    def __str__(self):
        return f'{
            self.user} as {
                self.get_role_display()} in {
                    self.context}({self.get_status_display()})'

    # Meta
    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")
        indexes = [
            models.Index(fields=['user', 'role', 'status']),
            models.Index(fields=['content_type', 'object_id', 'role']),
        ]
        # For PostgreSQL, you can add a conditional
        # UniqueConstraint for active bindings.
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'content_type', 'object_id', 'role'],
                condition=models.Q(status='active'),
                name='unique_active_membership'
            )
        ]
