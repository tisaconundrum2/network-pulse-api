"""Serialize the models"""
from rest_framework import serializers

from pulseapi.users.models import (
    EmailUser,
    UserFavorites,
)


class UserFavoritesSerializer(serializers.ModelSerializer):
    """
    Serializes a {user,entry,when} fave.
    """

    class Meta:
        """
        Meta class. Again: because
        """
        model = UserFavorites

class EmailUserSerializer(serializers.ModelSerializer):
    """
    Serializes an EmailUser...
    """

    email = serializers.EmailField()
    name = serializers.CharField(max_length=1000)
    is_staff = serializers.BooleanField(default=False)
