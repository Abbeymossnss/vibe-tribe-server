from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tribeapi.models import HelpTicket, Event, TribeUser, Status


class TicketView(ViewSet):
    #  vibetribe helptickets view
    # create view all to auth everybody to see all tickets!
    # retreive for everyone
    # update.. staff can update status and volunteer
    # not staff can update title and details
    # delete for non staff, only their tickets.
    def destroy(self, request, pk=None):
        # Handle delete requests for tickets
        # Ensure that the user is not a staff member
        if request.user.is_staff:
            return Response({"error": "Staff members cannot delete tickets."}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the tribe user instance associated with the requesting user
        tribe_user_instance = TribeUser.objects.get(user=request.user)

        try:
            # Attempt to retrieve the ticket with the given ID
            ticket = HelpTicket.objects.get(pk=pk)

            # Check if the requesting user is the creator of the ticket
            if ticket.creator != tribe_user_instance:
                return Response({"error": "You are not authorized to delete this ticket."}, status=status.HTTP_403_FORBIDDEN)

            # Delete the ticket
            ticket.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except HelpTicket.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        tickets = HelpTicket.objects.all()

        serialized = TicketSerializer(tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):

        try:
            ticket = HelpTicket.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def create(self, request):
        # Create a tribe user instance associated with the requesting user.
        creator_instance = TribeUser.objects.get(user=request.user)

        # Check if requesting user is staff/volunteer
        if request.user.is_staff:
            return Response({"error": "Be the problem SOLVER, not the problem starter."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure the event ID provided in the request corresponds to a valid event
        try:
            event = Event.objects.get(pk=request.data["event"])
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is the creator of the event
        if event.host != creator_instance:
            return Response({"error": "You can only create a ticket for events you own."}, status=status.HTTP_403_FORBIDDEN)

        # Create the ticket
        ticket = HelpTicket.objects.create(
            title=request.data["title"],
            issue=request.data["issue"],
            event=event,
            creator=creator_instance,
            # status=Status.objects.get(pk=request.data["status"]),
        )

        serializer = TicketSerializer(ticket)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'type',)


class VibeTribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TribeUser
        fields = ('id', 'full_name',)


class EventTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name',)


class TicketSerializer(serializers.ModelSerializer):
    creator = VibeTribeSerializer(many=False)
    volunteer = VibeTribeSerializer(many=False)
    status = StatusSerializer(many=False)
    event = EventTicketSerializer(many=False)

    class Meta:
        model = HelpTicket
        fields = ( 'id','title', 'issue', 'creator', 'status', 'volunteer', 'event')
