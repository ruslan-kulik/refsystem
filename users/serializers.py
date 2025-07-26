from rest_framework import serializers
from .models import CustomUser


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)


class ActivateInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)


class ProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    invited_by = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'phone_number',
            'invite_code',
            'invited_by',
            'invited_users',
            'first_name',
            'last_name',
            'email',
        ]

    def get_invited_users(self, obj):
        return [
            {
                'phone_number': u.phone_number,
                'invite_code': u.invite_code,
            }
            for u in obj.invited_users.all()
        ]

    def get_invited_by(self, obj):
        if obj.invited_by:
            return {
                'phone_number': obj.invited_by.phone_number,
                'invite_code': obj.invited_by.invite_code,
            }
        return None
