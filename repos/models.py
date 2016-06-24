from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=55, blank=False, unique=True)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

