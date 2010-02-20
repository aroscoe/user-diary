from django.contrib import admin
from story.models import *

admin.site.register(Story)
admin.site.register(StoryImage)

admin.site.register(TestStory)
admin.site.register(TestImage)