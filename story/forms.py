from django.forms import ModelForm
from story.models import Story, TestImage
from story.multi_file_field import MultiFileField

class StoryForm(ModelForm):
  images = MultiFileField(required=False)
  
  class Meta:
    model = Story
    exclude = ('user',)

class TestImageForm(ModelForm):
  class Meta:
    model = TestImage
