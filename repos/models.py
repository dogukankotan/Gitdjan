from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_delete, post_save
from pygit2 import init_repository

# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=55, blank=False, unique=True)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


def post_save_repository(sender, instance, *args, **kwargs):
    from gitdjan.settings import GITS_DIR
    path = GITS_DIR + instance.name
    init_repository(path, bare=True)

def post_delete_repository(sender, instance, *args, **kwargs):
    from shutil import rmtree
    from gitdjan.settings import GITS_DIR
    path = GITS_DIR + instance.name
    try:
        rmtree(path)
    except:
        pass

post_save.connect(post_save_repository, sender=Repository)
post_delete.connect(post_delete_repository, sender=Repository)

