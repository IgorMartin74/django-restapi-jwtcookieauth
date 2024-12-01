"""
Serializers for user-related functionality.
"""

from django.db import transaction
from django.contrib.auth import (
    get_user_model,
)

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a user with encrypted password and return the user."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a user and return it."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    

class CustomRegisterSerializer(RegisterSerializer):
    """Custom serializer for user registration."""

    name = serializers.CharField(max_length=255)

    # Define transation.atomic to rollback the save operation in case of er
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.name = self.data.get("name")
        user.save()
        return user