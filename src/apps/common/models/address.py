from django.db import models
from django.utils.translation import gettext_lazy as _
import re
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from localflavor.br.models import BRStateField


def validate_brazilian_zipcode(value):
    """ Validate a Brazilian ZIP code.
    """
    numbers = re.sub(r'\D', '', str(value))
    if len(numbers) != 8:
        raise ValidationError(_(
            "Invalid Brazilian ZIP code format. Use 00000-000"))


class Address(models.Model):
    """
    address model
    """

    class AddressesTypeChoices(models.TextChoices):
        HOME = 'home', _('Home')
        WORK = 'work', _('Work')
        BILLING = 'billing', _('Billing')
        SHIPPING = 'shipping', _('Shipping')
        OTHER = 'other', _('Other')

    address_type = models.CharField(
        max_length=25,
        verbose_name=_("address type"),
        choices=AddressesTypeChoices.choices,
        default=AddressesTypeChoices.HOME,
        help_text=_("Purpose of this address")
        )

    # Address Details
    country = CountryField(
        verbose_name=_("country"),
        default="BR",
        blank_label=_("Select a country"),
        )

    state = BRStateField(
        verbose_name=_("state"),
        blank=True,
        blank_label=_("Select a state"),
        null=True,
        )

    city = models.CharField(
        max_length=100,
        verbose_name=_("city")
        )

    district = models.CharField(
        max_length=100,
        verbose_name=_("district"),
        help_text=_("Neighborhood or district name"),
        )

    street = models.CharField(
        max_length=200,
        verbose_name=_("street"),
        validators=[MinLengthValidator(3)],
        help_text=_("Street name and number"),
        )

    number = models.CharField(
        max_length=10,
        verbose_name=_("number"),
        validators=[
            RegexValidator(
                r'^(\d+|S/N)$',
                message=_("Number must contain digits or be 'S/N'.")
            )
        ],
        help_text=_("Building/house number. Use 'S/N' for no number."),
        )

    complement = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("complement"),
        help_text=_("Apartment, floor, block, etc.")
        )

    zip_code = models.CharField(
        max_length=20,
        verbose_name=_("zip code"),
        help_text=_("ZIP code"),
        )

    class Meta:
        abstract = True
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ["city", "street"]

    def clean(self):
        """Validations and standardizations"""
        super().clean()
        errors = {}

        # standardization fields
        if self.street:
            self.street = self.street.strip()

        if self.city:
            self.city = self.city.strip()

        if self.district:
            self.district = self.district.strip()
        self.complement = (
            self.complement or "").strip()

        if self.number and self.number.upper() != 'S/N':
            if not any(c.isdigit() for c in self.number):
                errors['number'] = _(
                    "House number should contain at l"
                    "east one digit unless it's 'S/N'."
                )
        # Validation for Brazil
        if self.country.code == 'BR':
            # Validação do CEP usando a função existente
            try:
                validate_brazilian_zipcode(self.zip_code)
                # Formatação manual
                numbers = re.sub(r'\D', '', str(self.zip_code))
                if len(numbers) == 8:
                    self.zip_code = f"{numbers[:5]}-{numbers[5:]}"
            except ValidationError as e:
                errors['zip_code'] = str(e)

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # Utilitarian properties
    @property
    def full_address(self):
        parts = []

        # Street and number
        street = (self.street or "").strip()
        number = (self.number or "").strip()
        if street:
            if number and number.upper() != "S/N":
                parts.append(f"{street}, {number}")
            else:
                parts.append(street)

        # Complement and district
        if self.complement:
            parts.append(self.complement)
        if self.district:
            parts.append(self.district)

        # City - State
        city_state = [part for part in [
            (self.city or "").strip(), (self.state or "").strip()] if part
            ]

        if city_state:
            parts.append(" - ".join(city_state))

        # ZIP code
        if self.zip_code:
            parts.append(self.zip_code)  # já formatado pelo clean()

        # Country (only if not Brazil)
        if self.country.code != 'BR':
            parts.append(str(self.country.name))

        return ", ".join(parts)


