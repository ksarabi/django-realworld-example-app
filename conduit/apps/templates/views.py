from django.shortcuts import render
from rest_framework import generics
from .serializers import TemplateSerializer
from .models import Template


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new Template."""
        serializer.save()

