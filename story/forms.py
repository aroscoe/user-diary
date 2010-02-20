from django.forms import ModelForm
from story.models import Story, TestImage, TestStory
from story.multi_file_field import MultiFileField, MultiFileInput

class StoryForm(ModelForm):
    class Meta:
        model = Story
        exclude = ('images','user',)

class TestStoryForm(ModelForm):
  images = MultiFileField()
  
  class Meta:
    model = TestStory

class TestImageForm(ModelForm):
  class Meta:
    model = TestImage
