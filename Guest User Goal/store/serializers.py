from rest_framework import serializers
from .models import (Customer
                     )


class CustomerSerializer(serializers.ModelSerializer):
    """
    Class for serializing country list.
    """
    class Meta:
        model = Customer
        fields = ["id", "user", "name", "email"]


