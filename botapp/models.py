"""Python script for creating the database."""
# python manage.py makemigrations botapp
# python manage.py migrate
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from botapp.helper.helper import generate_filename

class Bot(models.Model):
    AVAILABILITY_CHOICES = (
        ('N', 'None'),
        ('U', 'Users'),
        ('E', 'Everyone')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_set')
    avtaar = models.FileField(upload_to=generate_filename, blank=True, null=True)
    brain = models.FileField(upload_to=generate_filename, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(max_length=128, blank=True, null=True)
    visible = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    chatlog = models.FileField(upload_to=generate_filename, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']