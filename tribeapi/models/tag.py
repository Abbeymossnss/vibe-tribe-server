from django.db import models


class Tag(models.Model):
    """game type model class"""
    label = models.CharField(max_length=50)
