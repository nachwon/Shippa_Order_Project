from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from merchants.models import Merchant, Menu
from merchants.enums import BinaryOfDays, MAPPING_OF_AVAILABLE_DAYS, AVAILABLE_COUNTRY_ISO_LIST, AVAILABLE_CURRENCIES


def _validate_time_format(value):
    try:
        datetime.strptime(value, "%H:%M:%S")
    except ValueError:
        raise ValidationError
    return value


def _convert_to_binary_for_business_days(value):
    if not isinstance(value, list):
        raise ValidationError
    try:
        ret = sum([BinaryOfDays[day].value for day in value])
    except KeyError:
        raise ValidationError
    return ret


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            'id', 'name', 'email', 'phone', 'forced_closing', 'business_days',
            'open_time', 'close_time', 'country_iso', 'city', 'detail_address',
            'created_at',
        ]
        read_only_fields = [
            'id', 'created_at',
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['business_days'] = MAPPING_OF_AVAILABLE_DAYS.get(ret['business_days'], [])
        return ret

    def validate_country_iso(self, value):
        try:
            value = str(value)
        except (ValueError, TypeError):
            raise ValidationError

        value = value.upper()
        if value not in AVAILABLE_COUNTRY_ISO_LIST:
            raise ValidationError(f'\'{value}\' is not supported country.')
        return value

    def to_internal_value(self, data):
        if data.get('business_days'):
            data['business_days'] = _convert_to_binary_for_business_days(data['business_days'])
        ret = super().to_internal_value(data)
        return ret


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'image', 'price', 'currency', 'quantity', 'merchant_id', 'closed',
            'created_at',
        ]
        read_only_fields = [
            'id', 'merchant_id', 'created_at',
        ]

    def validate_currency(self, value):
        try:
            value = str(value)
        except (ValueError, TypeError):
            raise ValidationError

        value = value.upper()
        if value not in AVAILABLE_CURRENCIES:
            raise ValidationError(f'\'{value}\' is not supported currency.')
        return value

    def validate_quantity(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError

        if value < 0:
            raise ValidationError('quantity must be positive integer.')

        return value

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['merchant_id'] = self.context['merchant_id']
        return ret
