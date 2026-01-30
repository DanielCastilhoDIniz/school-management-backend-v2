from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.common.models.base import Base
from src.apps.users.models import CustomUser

from apps.common.models.address import Address

from django.core.exceptions import ValidationError

from datetime import date
import re
from django.core.validators import RegexValidator


def validate_cnpj(value):
    """Valida formato e dígitos de
    CNPJ (00.000.000/0000-00 ou 00000000000000)
    """
    if not value:
        return
    cnpj = re.sub(r'\D', '', str(value))
    if len(cnpj) != 14:
        raise ValidationError(
            _("CNPJ deve conter exatamente 14 dígitos numéricos."))


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


class AddressNetSchools(Address):
    net_school_address = models.ForeignKey(
        'NetSchools',
        related_name='addresses',
        verbose_name=_("net_school_address"),
        on_delete=models.PROTECT,
        help_text=_("address of the school network")
    )

    class Meta:
        verbose_name = _("Net School Address")
        verbose_name_plural = _("Net School Addresses")


class NetSchools(Base):
    """
        It registers an educational network of any size,
        from one unit up to however many exist,
        here we are dealing with the main unit
    """

    parent_company_name = models.CharField(
        max_length=100,
        verbose_name=_("name of the parent company")
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
        max_length=18,  # suficiente para 00.000.000/0000-00
        unique=True,
        verbose_name=_("CNPJ"),
        validators=[
            RegexValidator(
                r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$|^\d{14}$',
                message=_(
                    "Invalid format for CNPJ."
                    "Use 00.000.000/0000-00 ou 00000000000000."),
            ),
            validate_cnpj,
        ],
    )
    foundation_date = models.DateField(
        verbose_name=_("foundation_date"),
        )

    class Meta:
        app_label = 'institutions'
        verbose_name = _("School Network")
        verbose_name_plural = _("School Networks")
        ordering = ["trade_name"]
        db_table_comment = "Educational institution networks"
        indexes = [
            models.Index(fields=['trade_name']),
            models.Index(fields=['legal_name']),
            ]

    # validators
    def clean(self):
        super().clean()

        if self.parent_company_name:
            self.parent_company_name = self.parent_company_name.strip()

        if self.legal_name:
            self.legal_name = self.legal_name.strip().upper()

        if self.trade_name:
            self.trade_name = self.trade_name.strip()

        if self.foundation_date and self.foundation_date > date.today():
            raise ValidationError({
                'foundation_date': _('Date cannot be in the future.')
            })

    def __str__(self):
        return self.trade_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
