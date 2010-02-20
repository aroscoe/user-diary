from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Story(models.Model):
  place           = models.CharField(max_length=150)
  people_involved = models.TextField(blank=True)
  images          = models.ManyToManyField('StoryImage', blank=True)
  date_posted     = models.DateTimeField(auto_now_add=True)
  user            = models.ForeignKey(User)
  
  class Admin:
    pass
  
class StoryImage(models.Model):
  image = models.FileField(upload_to=settings.UPLOADS_DIR)
  
  class Admin:
    pass

class TestStory(models.Model):
  name = models.CharField(max_length=150)
  images = models.ManyToManyField('TestImage')
  
  class Admin:
    pass

class TestImage(models.Model):
  image = models.FileField(upload_to='test')
  
  class Admin:
    pass
    
