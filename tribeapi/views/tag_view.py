from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tribeapi.models import Tag, TribeUser


class TagView(ViewSet):
    # vibetribe tag view

    def destroy(self, request, pk=None):
        # handle delete requests for events
        # authorize only users whos is_staff=false.
        # return no response, with 204 status code.

        # check if user is staff.
        if request.auth.user.is_staff:
            return Response({"error": "You are not authorized to be a party pooper."}, status=status.HTTP_403_FORBIDDEN)

        # now delete the event! and return a 204 no response
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        """Returns: Response:None. with 204 status code"""
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        #    Handle GET requests to get all events
        #  Returns: Response -- JSON serialized list of events.

        tags = Tag.objects.all()

        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """Handle GET requests for single game type"""
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)

        return Response(serializer.data)

    def create(self, request):
        # will still need authorize if statement. and host instance.
        if request.user.is_staff:
            return Response({"error": "It takes an actual HOST to throw a party... DUH."}, status=status.HTTP_403_FORBIDDEN)

        tag = Tag.objects.create(
            label=request.data["label"]
        )

        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):

        if request.user.is_staff:
            return Response({"error": "If you're not a host, you shouldn't meddle."}, status=status.HTTP_403_FORBIDDEN)
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

        tag.label = request.data.get["label", tag.label]

        # Save the updated event
        tag.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'label',)
        depth = 1
