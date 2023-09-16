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

    def destroy(self, request, pk=None):
        # Handle delete requests for events
        # Authorize only users who are not staff (is_staff=False) to delete their own events
        # Return no response, with 204 status code.

        tribe_user_instance = TribeUser.objects.get(user=request.user)

        # Check if user is staff.
        if not request.auth.user.is_staff:
            # User is not a staff member, proceed to delete their event.
            try:
                event = Event.objects.get(pk=pk, host=tribe_user_instance)
                event.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Event.DoesNotExist:
                return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "You are not authorized to delete this event."}, status=status.HTTP_403_FORBIDDEN)


    def list(self, request):
        #    Handle GET requests to get all events
        #  Returns: Response -- JSON serialized list of events.
        tribe_user_instance= TribeUser.objects.get(user=request.user)

        if request.auth.user.is_staff:
            events = Event.objects.all()

        else:
            events = Event.objects.filter(host=tribe_user_instance)
            

        serialized = EventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
    # Retrieve the event
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is staff
        if request.user.is_staff:
            return Response({"error": "Staff members are not allowed to access this view."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize and return the event
        serializer = EventSerializer(event)
        return Response(serializer.data)
        
    def create(self, request):
        # you'll need if statement to authorize only non staff members to be able to create a new event.
        # must create a tribeuser instance to compare to django user. apples to apples.
        # fk's in this will be tags, and host.
        # retrieve the tags by their id's
        # remember.. many tags, on many events. so be sure to set many=true.
        
        # handle post operations
            # returns response --JSON serialized tribe user host instance
        
        # check if requesting user is staff/volunteer
        if request.user.is_staff:
            return Response({"error": "It takes an actual HOST to throw a party... DUH."}, status=status.HTTP_403_FORBIDDEN)

        
        # create a tribe user instance associated with requesting user.
        host_instance = TribeUser.objects.get(user=request.user)

        # retrieve the tag objects based on provided tag ID's
        tag_ids = request.data.get("tags", [])
        tags = Tag.objects.filter(pk__in=tag_ids)

        #   do i need this? check if any of requested tags do not exist.
        if len(tags) != len(tag_ids):
            return Response({"error": "Umm.. pick a #tag, ANY #tag, but don't go making them up!"}, status=status.HTTP_400_BAD_REQUEST)

    # Create event if user is not a staff member.
        event = Event.objects.create(
            name=request.data["name"],
            details=request.data["details"],
            location=request.data["location"],
            date=request.data["date"],
            time=request.data["time"],
            host=host_instance,
        )

        # add the tags to the event.
        event.tags.set(tags)

    # serialize and return created event.
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        # handle put requests for single event.
        # returns response. no body, just 204 status code.
        # authorize host(not staff) to make edits to their event. use if statement to check.
        # then create tribe user host instance for Django user. apples to apples
        # fk's are host_id and tags.
        # remember tags is many to many.. so must use an array [] to hold multiple tag_id's.
        # set the many to many to event.. 
        # annnd save!

        # check if requested user is staff.
        if request.user.is_staff:
            return Response({"error": "If you're not a host, you shouldn't meddle."}, status=status.HTTP_403_FORBIDDEN)

        # # create a tribe user instance associated with requesting user.
        # host_instance = TribeUser.objects.get(user=request.user)

        # retrieve the event to update. do i need to do it this way?
        # select the targeted event to edit using pk"""
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        # # Check if the requesting user is the host of the event. THIS IS SECURITY ASSURANCE BUT IS PROBABLY REDUNDANT
        # if event.host != host_instance:
        #     return Response({"error": "You are not the host of this event, and you cannot edit it."}, status=status.HTTP_403_FORBIDDEN)

        # Update the event fields based on the request data!
        event.name = request.data.get("name", event.name)
        event.details = request.data.get("details", event.details)
        event.location = request.data.get("location", event.location)
        event.date = request.data.get("date", event.date)
        event.time = request.data.get("time", event.time)

        # Retrieve the tag objects based on the provided tag ID's ***research about this pk__in=****
        tag_ids = request.data.get("tags", [])
        tags = Tag.objects.filter(pk__in=tag_ids)

        # set the tags for the event (many to many)
        event.tags.set(tags)
        
        # Save the updated event
        event.save()

        # Serialized that ish.. then return
        # Return a 204 No Content response without a response body
        return Response(status=status.HTTP_204_NO_CONTENT)

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
