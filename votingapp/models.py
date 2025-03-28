from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class User(AbstractUser):
#     pass

class Topic(models.Model):
    topic = models.CharField(max_length= 300)
    pub_date = models.DateTimeField('Date published')
    
    def __str__(self):
        return self.topic
    
class Options(models.Model):
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    options_text= models.CharField(max_length =200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.options_text
