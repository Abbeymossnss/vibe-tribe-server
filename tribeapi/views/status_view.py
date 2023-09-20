from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tribeapi.models import Event, TribeUser, HelpTicket, Status


class StatusView(ViewSet):

    def destroy(self, request, pk=None):

        if request.auth.user.is_staff:
            return Response({"error": "You are not authorized to be a party pooper."}, status=status.HTTP_403_FORBIDDEN)

        statuz = Status.objects.get(pk=pk)
        statuz.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):

        statuz = Status.objects.all()

        serialized = StatusSerializer(statuz, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):

        statuz = Status.objects.get(pk=pk)
        serializer = StatusSerializer(statuz)

        return Response(serializer.data)
    
    def create(self, request):
        
        if request.user.is_staff:
            return Response({"error": "Be the solution...Not the problem DUH."}, status=status.HTTP_403_FORBIDDEN)

        statuz = Status.objects.create(
            type=request.data["type"]
        )

        serializer = StatusSerializer(statuz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self,request, pk=None):
        
        try:
            statuz = Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            return Response({"error": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

        statuz.type = request.data.get["status", statuz.type]

        # Save the updated event
        statuz.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'type',)
        depth = 1
