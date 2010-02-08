from django.forms import ModelForm
from story.models import Story

class StoryForm(ModelForm):
    class Meta:
        model = Story
        exclude = ('images','user',)