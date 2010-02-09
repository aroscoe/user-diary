from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from story.forms import StoryForm
from story.models import Story as StoryModel
from story.models import StoryImage as StoryImageModel

from story import my_debug

@login_required
def add_story(request):
  if request.method == 'POST':
    form = StoryForm(request.POST)
    
    if form.is_valid():
      story = form.save(commit=False)
      
      # add user name
      story.user = request.user
      story.save()
      
      # add image 
      # TODO: change to add multiple images
      image_file = _handle_uploaded_file(request.FILES['image'])
      image = StoryImageModel.objects.create(image=image_file)
      story.images.add(image)
      
      return render_to_response('success.html')
  else:
    form = StoryForm()
  return direct_to_template(request, 'story/add.html', locals())

def _handle_uploaded_file(file):
  file_path = settings.UPLOADS_DIR + file.name
  destination = open(file_path, 'wb+')
  for chunk in file.chunks():
      destination.write(chunk)
  destination.close()
  return file_path