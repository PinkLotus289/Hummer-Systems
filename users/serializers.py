from rest_framework import serializers
from .models import User

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Номер телефона должен начинаться с '+'.")
        digits_part = value[1:]
        if not digits_part.isdigit():
            raise serializers.ValidationError("После '+' номер должен содержать только цифры.")
        if len(value) > 15:
            raise serializers.ValidationError("Номер телефона не должен превышать 15 символов.")
        return value


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)

    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Номер телефона должен начинаться с '+'.")
        digits_part = value[1:]
        if not digits_part.isdigit():
            raise serializers.ValidationError("После '+' номер должен содержать только цифры.")
        if len(value) > 15:
            raise serializers.ValidationError("Номер телефона не должен превышать 15 символов.")
        return value

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Код должен содержать только цифры.")
        if len(value) != 4:
            raise serializers.ValidationError("Код должен состоять из 4 цифр.")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'used_invite_code', 'invited_users']

    def get_invited_users(self, obj):
        users = User.objects.filter(used_invite_code=obj.invite_code).values_list('phone_number', flat=True)
        return list(users)


class UseInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Инвайт‑код может содержать только буквы и цифры.")
        if len(value) != 6:
            raise serializers.ValidationError("Инвайт‑код должен состоять из 6 символов.")
        return value
