from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
Model for individual task's that will be latter added to Zone model.
"""
class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


# Zone model for diferent zones that has diferent tasks for each zone
