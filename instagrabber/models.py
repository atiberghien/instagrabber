# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager

from django.core.cache import cache

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class InstaConfig(SingletonModel):
    
    search_accounts = models.CharField(max_length=500, default='instagram', help_text="Comptes séparés par une virgule sans le @.")
    search_hashtags = models.CharField(max_length=500, default='instagram', help_text="Hashtags séparés par une virgule sans le #.")
    
    backlist = models.CharField(max_length=500, null=True, blank=True, help_text="Comptes séparés par une virgule, sans le @.")
    notif_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return "Configuration Instagram"

class InstaUser(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

class InstaPicture(models.Model):
    instagram_id = models.CharField(max_length=100, unique=True)
    instagram_url = models.CharField(max_length=500)
    caption = models.TextField(default="")
    user = models.ForeignKey(InstaUser, null=True, blank=True, on_delete=models.SET_NULL)
    likes = models.PositiveIntegerField(default=0)
    datetime = models.DateTimeField()
    tags = TaggableManager()

    selected = models.BooleanField(default=False)

    class Meta:
        ordering = ('-datetime',)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=InstaConfig)
def delete_blacklisted(sender, instance, **kwargs):
    blacklist = instance.backlist.replace(' ','').split(',')
    InstaUser.objects.filter(username__in=blacklist).delete()
