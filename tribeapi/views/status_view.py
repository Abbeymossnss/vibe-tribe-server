from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tribeapi.models import Event, TribeUser, HelpTicket, Status


class StatusView(ViewSet):
    
    def list(self, request):
        status = Status.objects.all()

        serialized = StatusSerializer( statuss, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)