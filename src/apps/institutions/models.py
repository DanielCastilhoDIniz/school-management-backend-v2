from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.common.models import Base
from src.apps.users.models import CustomUser


class InstitutionChoicesType(Base):
    institution_choices_type_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("institution_choices_type"),
        help_text=_("Name of the institution types")
        )
    description = models.TextField(
        blank=True,
        max_length=200,
        verbose_name=_("description")
        )

    def __str__(self):
        return self.institution_choices_type_name

    class Meta:
        verbose_name = _("Institution Type")
        verbose_name_plural = _("Institution Types")
        ordering = ["institution_choices_type_name"]
        db_table = "institution_types"
        db_table_comment = "institution_types table, used by only Institutions"


class NetSchools(Base):

    parent_company_name = models.CharField(
        max_length=100,
        verbose_name=_("parent_company_name")
        )

    owner = models.ForeignKey(
        CustomUser,
        related_name='school_networks',
        verbose_name=_("owner"),
        on_delete=models.PROTECT,
        help_text=_("Find")
    )
    institution_type = models.ForeignKey(
        InstitutionChoicesType,
        related_name='networks',
        verbose_name=_("institution_type"),
        on_delete=models.PROTECT
        )
    legal_name = models.CharField(
        max_length=100,
        verbose_name=_("legal_name")
        )
    trade_name = models.CharField(
        max_length=100,
        verbose_name=_("trade_name")
        )
    tax_identification_number = models.CharField(
        max_length=14,
        unique=True,
        verbose_name=_("tax identification number")
        )
    foundation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("foundation_date")
        )

    class Meta:
        verbose_name = _("School Network")
        verbose_name_plural = _("School Networks")
        ordering = ["trade_name"]
        db_table = "school_networks"
        db_table_comment = "Educational institution networks"