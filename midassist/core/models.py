"""
This module represent the models of MedAssist
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Member(models.Model):
    """
    Member Model Fields
    """
    first_name = models.TextField()
    last_name = models.TextField()
    age = models.IntegerField()
    email = models.EmailField()
    contact_number = models.CharField(max_length=10)
    password = models.TextField()
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """
        Member Meta Data
        """
        ordering = ['created']


# core/models.py

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
