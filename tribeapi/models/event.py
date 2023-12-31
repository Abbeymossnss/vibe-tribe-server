from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=1000)
    location = models.CharField(max_length=50,null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    host = models.ForeignKey("TribeUser", null=True, blank=True,
    on_delete=models.CASCADE, related_name="tribeUser_host")
    tags = models.ManyToManyField(
        "Tag", through="EventTag", related_name="event_tags")
    
# had to go back and add model property.. location!! remember to migrate that change!