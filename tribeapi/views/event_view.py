from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tribeapi.models import Event, TribeUser, Tag

# use honey rae's customer view to help you retreive all events, authenticated is staff can see all.
# is_staff=false can only see events they created.
# you will need to serialize the tribeUser and the tags.


class EventView(ViewSet):
    # vibetribe evens view

    # def retrieve(self, request, pk):
    #     # this handles GET requests for a single event"
    #     event = Event.objects.get(pk=pk)
    #     serializer = EventSerializer(event)

    # return Response(serializer.data)

    def list(self, request):
        #    Handle GET requests to get all events
        #  Returns: Response -- JSON serialized list of events.

        events = []

        if request.auth.user.is_staff:
            events = Event.objects.all()

        else:
            events = Event.objects.filter(tribe_User=request.auth.user)

        serialized = EventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class TribeUserHostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TribeUser
        fields = ('id', 'user', 'bio', 'img_url', 'full_name',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'label',)


class EventSerializer(serializers.ModelSerializer):
    # JSON serializer for tribeUsers
    host = TribeUserHostSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'details', 'location',
                  'date', 'time', 'host', 'tags')
        depth = 1
