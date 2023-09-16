from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from tribeapi.models import TribeUser


class TribeUserViewSet(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tribe_user
        Returns:
            Response -- JSON serialized tribe_user
        """
        tribe_user = TribeUser.objects.get(pk=pk)
        serializer = TribeUserSerializer(tribe_user)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all profiles

        Returns:
            Response -- JSON serialized list of profiles
        """
        tribe_users = TribeUser.objects.all()
        serializer = TribeUserSerializer(tribe_users, many=True)
        return Response(serializer.data)


class TribeUserSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    class Meta:
        model = TribeUser
        fields = ('id', 'bio','full_name', 'img_url', 'is_staff',)

