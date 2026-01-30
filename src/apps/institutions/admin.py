from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from .models.models_net import (
    InstitutionChoicesType,
    NetSchools,
    AddressNetSchools)


@admin.register(InstitutionChoicesType)
class InstitutionChoicesTypeAdmin(admin.ModelAdmin):
    list_display = [
        'institution_choices_type_name',
        'description'
    ]
    search_fields = [
        'institution_choices_type_name',
        'description',
    ]
    ordering = [
        'institution_choices_type_name',
    ]


class AddressNetSchoolsInline(admin.StackedInline):
    model = AddressNetSchools
    extra = 0
    show_change_link = True

    readonly_fields = [
        'full_address',
    ]

    fieldsets = (
        (_("Address type"), {
            "fields": ("address_type",),
        }),
        (_("Location"), {
            "fields": ("country", "state", "city", "district"),
        }),
        (_("Street"), {
            "fields": ("street", "number", "complement"),
        }),
        (_("Postal"), {
            "fields": ("zip_code",),
        }),
        (_("Formatted"), {
            "fields": ("full_address",),
        }),
    )


@admin.register(NetSchools)
class NetSchoolsAdmin(admin.ModelAdmin):
    inlines = [
        AddressNetSchoolsInline,
    ]

    @admin.display(description=_("Owner Name"), ordering='owner__username')
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() or obj.owner.username

    list_display = [
        'trade_name',
        'parent_company_name',
        'legal_name',
        'institution_type',
        'get_owner_name',
        'tax_identification_number',
        'foundation_date',
    ]
    search_fields = [
        'trade_name',
        'legal_name',
        'parent_company_name',
        'tax_identification_number',
        'owner__username',
        'foundation_date',
    ]

    list_filter = (
        'institution_type',
        'foundation_date',
    )
    ordering = [
        'trade_name',
    ]