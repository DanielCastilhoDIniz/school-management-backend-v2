from rest_framework import serializers
from ..models import NetSchools, AddressNetSchools

import re


class AddressNetSchoolsSerializer(serializers.ModelSerializer):
    """
    Address are auxiliary data, loaded on demand,
    They are not  part of the application's path
    """

    formatted_address = serializers.ReadOnlyField(source='full_address')

    class Meta:
        model = AddressNetSchools
      
        fields = [
            'address_type',
            'country',
            'state',
            'city',
            'district',
            'street',
            'number',
            'complement',
            'zip_code',
            'formatted_address',
        ]
        extra_kwargs = {
                "complement": {"required": False, "allow_blank": True},
                "district": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs):
        if attrs['country'].code == 'BR' and not attrs.get('state'):
            raise serializers.ValidationError(
                {"state": "Estado é obrigatório para endereços no Brasil"}
            )
        return attrs


class NetSchoolsSerializer(serializers.ModelSerializer):

    addresses = AddressNetSchoolsSerializer(many=True, read_only=True)
    owner_name = serializers.ReadOnlyField(source='owner.username')
    institution_type_name = serializers.ReadOnlyField(
        source='institution_type.institution_choices_type_name')

    class Meta:
        model = NetSchools
        fields = [
            'parent_company_name',
            'legal_name',
            'trade_name',
            'tax_identification_number',
            'foundation_date',
            'institution_type_name',
        ]

    def validate_tax_identification_number(self, value):
        numbers = re.sub(r'\D', '', value)
        if len(numbers) != 14:
            raise serializers.ValidationError("CNPJ inválido")
        return numbers
