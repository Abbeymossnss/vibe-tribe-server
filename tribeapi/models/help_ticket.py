from django.db import models

class HelpTicket(models.Model):
    title = models.CharField(max_length=50)
    issue = models.CharField(max_length=500)
    creator = models.ForeignKey("TribeUser", 
                                on_delete=models.CASCADE, related_name="submitted_tickets")
    volunteer = models.ForeignKey("TribeUser",  null=True, blank=True,
                                  on_delete=models.CASCADE, related_name="assigned_tickets")
    status = models.ForeignKey("Status", null=True, blank=True,
                               on_delete=models.CASCADE, related_name="ticket_status")
    event_id = models.ForeignKey("Event", null=True, blank=True,
                                on_delete=models.CASCADE, related_name="ticket_event")


    # i changed the original details property to "issue"
    # ticket_ event means the party event that the ticket is for.
    # ticket_creator is the id of the host that has created the help ticket and needs the help
    # ticket_volunteer is the id of the volunteer that will be solving/completing the ticket submitted
    # ticket_status, the current status of the ticket, whether its in progress, or completed 
