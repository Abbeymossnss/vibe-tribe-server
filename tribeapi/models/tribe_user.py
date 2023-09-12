from django.db import models
from django.contrib.auth.models import User


class TribeUser(models.Model):

    # Relationship to the built-in User model which has name and email and is staff
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional address field to capture from the client
    bio = models.CharField(max_length=155, null=True, blank=True)
    # Add the img_url property
    # Assuming the image URL is a URL field
    img_url = models.URLField(max_length=255, null=True, blank=True)


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
