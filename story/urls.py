from django.conf.urls.defaults import *
 
urlpatterns = patterns('story.views',
    # url(r'^$', 'add_story', name="story_add"),
    url(r'^add/', 'add_story', name="story_add"),
)