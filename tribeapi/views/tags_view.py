from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tribeapi.models import Tag


class TagView(ViewSet):

    def destroy(self, request, pk=None):
        # handle delete requests for events
        # authorize only users whos is_staff=false.
        # return no response, with 204 status code.

        # check if user is staff.
        if request.auth.user.is_staff:
            return Response({"error": "You are not authorized to be a party killer."}, status=status.HTTP_403_FORBIDDEN)

        # now delete the event! and return a 204 no response
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        """Returns: Response:None. with 204 status code"""
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request):
    #    Handle GET requests to get all events
    #  Returns: Response -- JSON serialized list of events.
        tribe_user_instance= TribeUser.objects.get(user=request.user)

        if request.auth.user.is_staff:
            tags = Tag.objects.all()

        else:
            tags= Tag.objects.filter(host=tribe_user_instance)
            

        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)