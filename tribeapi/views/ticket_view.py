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
        # Handle delete requests for events
        # Authorize only users who are not staff (is_staff=False) to delete their own events
        # Return no response, with 204 status code.

        tribe_user_instance = TribeUser.objects.get(user=request.user)

        # Check if user is staff.
        if not request.auth.user.is_staff:
            # User is not a staff member, proceed to delete their event.
            try:
                ticket = HelpTicket.objects.get(pk=pk, host=tribe_user_instance)
                ticket.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Event.DoesNotExist:
                return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "You are not authorized to delete this ticket."}, status=status.HTTP_403_FORBIDDEN)












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

        # create a tribe user instance associated with requesting user.
        creator_instance = TribeUser.objects.get(user=request.user)

# check if requesting user is staff/volunteer
        if request.user.is_staff:
            return Response({"error": "Be the problem SOLVER, not the problem starter."}, status=status.HTTP_403_FORBIDDEN)

    #     # Define the fields that non-staff members are allowed to create
    #     allowed_fields = ['title', 'issue', 'event']  # Add more fields as needed

    # # Create a dictionary of request data containing only allowed fields
    #     data = {field: request.data.get(field) for field in allowed_fields}

    # # Add the creator field (assuming it's not allowed to be set by the user)
    #     data['creator'] = creator_instance.id

        ticket = HelpTicket.objects.create(
            title=request.data["title"],
            issue=request.data["issue"],
            event=Event.objects.get(pk=request.data["event"]),
            creator=creator_instance
        )

        serializer = TicketSerializer(ticket)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):

        try:
            ticket = HelpTicket.objects.get(pk=pk)
        except HelpTicket.DoesNotExist:
            return Response({"error": "Help Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

# update fields based on the request data.
        ticket.title = request.data.get("title", ticket.title)
        ticket.issue = request.data.get("issue", ticket.issue)

        volunteer = TribeUser.objects.get(pk=request.data["volunteer"])
        ticket.volunteer = volunteer

        ticket_status = Status.objects.get(pk=request.data["status"])
        ticket.ticket_status = ticket_status
        ticket.save()

        return Response(None, status=status.HTTP_200_OK)

    



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
        fields = ('title', 'issue', 'creator', 'status', 'volunteer', 'event')
