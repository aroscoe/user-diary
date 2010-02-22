from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout

import os.path

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^story/', include('user-diary.story.urls'), name="story"),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'assets')}),
    )