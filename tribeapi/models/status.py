from django.db import models


class Status(models.Model):
    """game type model class"""
    type = models.CharField(max_length=50)
