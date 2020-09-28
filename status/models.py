import re


from django.db import models
from common.models import IndexedTimeStampedModel
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from Hashtag.signals import parsed_hashtags
from datetime import datetime, timedelta

User = get_user_model()


class StatusQuerySet(models.QuerySet):
    def get_messages(self, number, user=None):
        if user is not None:
            return self.filter(user=user).order_by('-id')[:number]
        return self.order_by('-id')[:number]

    def get_hastags(self, tag):
        return self.filter(message__icontains="#" + tag)

    def get_latest_messages(self):
        return self.order_by('user__id', '-created').distinct('user')


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)

    def get_messages(self, number, user=None):
        return self.get_queryset().get_messages(number, user)

    def get_hastags(self, tag):
        return self.get_queryset().get_hastags(tag)

    def delete_old_message_over_10_days(self):
        qs = self.objects.filter(
            created_date__lte=datetime.now()-timedelta(days=10))
        qs.delete()

    def get_latest_messages(self):
        return self.get_queryset().get_latest_messages()


class Status(IndexedTimeStampedModel):
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.message

    objects = StatusManager()

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "Status"


def status_save_receiver(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        # notify a user
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.message)

        # send notification to user here.
        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_regex, instance.message)
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)


post_save.connect(status_save_receiver, sender=Status)
