from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'points'
        ]
        read_only_fields = [
            'points'
        ]


class PointSerializer(serializers.ModelSerializer):
    points_spent = serializers.IntegerField(default=0)
    points_added = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = [
            'points_spent', 'points_added'
        ]

    def to_representation(self, instance):
        return {
            "points": instance.points
        }

    def validate_points_spent(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError({
                "points_spent": "points_spent should be a positive integer."
            })

        if value and value < 0:
            raise ValidationError("points_spent should be a positive integer.")

        return value

    def validate_points_added(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError({
                "points_added": "points_added should be a positive integer."
            })

        if value and int(value) < 0:
            raise ValidationError("points_added should be a positive integer.")

        return value

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        points_spent = data.get('points_spent', 0)
        points_added = data.get('points_added', 0)

        if not points_spent and not points_added:
            raise ValidationError(
                {"error": "No data to update."}
            )

        if points_spent and points_added:
            raise ValidationError(
                {"error": "It is not allowed to add and spend points at the same time."}
            )

        points = -points_spent if points_spent else points_added

        return {
            "points": points
        }

    def update(self, instance, validated_data):
        points = instance.points
        points_to_update = validated_data.get('points')
        calculated_points = points + points_to_update

        if calculated_points < 0:
            raise ValidationError({
                "points": "Not enough points."
            })

        instance.points = calculated_points
        instance.save()
        return instance
