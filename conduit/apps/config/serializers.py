from rest_framework import serializers
from .models import Config
class ConfigSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Config
        fields = ('id','name', 'content')