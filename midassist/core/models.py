
"""
This module represent the models of MedAssist
"""
from django.db import models

class TestDB(models.Model):
    """Create your models here."""
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        """
        Test Meta Data
        """
        ordering = ['-update']


class Member(models.Model):
    """
    Member Model Fields
    """
    first_name=models.TextField()
    last_name=models.TextField()
    age=models.IntegerField()
    email=models.EmailField()
    contact_number=models.CharField(max_length=10)
    password=models.TextField()
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """
        Member Meta Data
        """
        ordering=['created']
