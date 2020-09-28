from django.db import models
from status.models import  Status
from django.urls import reverse_lazy
from common.models import  IndexedTimeStampedModel
from .signals import  parsed_hashtags



class Hashtag(IndexedTimeStampedModel):
    tag = models.CharField(max_length=64)
    
    def __str__(self):
        return self.tag
    
    def get_messages(self):
        return Status.objects.get_hastags(self.tag)
   
    def get_absolute_url(self):
        return reverse_lazy("hashtag", kwargs={"hashtag": self.tag})
    
    
    
def parsed_hashtags_receiver(sender, hashtag_list, *args, **kwargs):
    if len(hashtag_list) > 0:
        for tag_var in hashtag_list:
            new_tag, create = Hashtag.objects.get_or_create(tag=tag_var)
            

parsed_hashtags.connect(parsed_hashtags_receiver)