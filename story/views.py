from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from story.forms import StoryForm
from story.models import Story as StoryModel

@login_required
def add_story(request):
  if request.method == 'POST':
    form = StoryForm(request.POST)
    
    if form.is_valid():
      completed_form = form.save(commit=False)
      completed_form.user = request.user
      completed_form.save()
      # image_file = self._handle_uploaded_file(request.FILES['file'])
      return render_to_response('success.html')
  else:
    form = StoryForm()
  return direct_to_template(request, 'form.html', locals())

def _handle_uploaded_file(self, file):
  file_path = settings.UPLOADS_DIR + file.name
  destination = open(file_path, 'wb+')
  for chunk in file.chunks():
      destination.write(chunk)
  destination.close()
  return file_path