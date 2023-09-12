from django.db import models


class EventTag(models.Model):
    event = models.ForeignKey("Event",on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag",on_delete=models.CASCADE)
