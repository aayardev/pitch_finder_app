import os

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import (
    UserDetailsSerializer,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()
CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "")


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    # profile_image = serializers.ImageField()

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        # user.profile_image = self.validated_data.get("profile_image")
        user.save()

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."),
            )
        return super().validate_email(email)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    full_name = serializers.CharField()

    class Meta(UserDetailsSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
        ]
        extra_kwargs = {"profile_image": {"write_only": True}}
