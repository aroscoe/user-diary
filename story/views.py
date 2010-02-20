from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from story.forms import StoryForm, TestImageForm, TestStoryForm
from story.models import Story as StoryModel
from story.models import StoryImage as StoryImageModel
from story.models import TestImage

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




def test_image(request):
  if request.method == 'POST':
    form = TestImageForm(request.POST, request.FILES)
    
    if form.is_valid():
      form.save()
      return render_to_response('success.html')
  else:
    form = TestImageForm()
  return direct_to_template(request, 'story/test.html', locals())

def test_story(request):
  if request.method == 'POST':
    form = TestStoryForm(request.POST, request.FILES)
    
    if form.is_valid():
      story = form.save(commit=False)
      # TODO: add user
      story.save()
      
      for image in form.cleaned_data['images']:
        saved_img = TestImage.objects.create(image=image)
        story.images.add(saved_img)
    
      story.save()
      return render_to_response('success.html')
  else:
      form = TestStoryForm()
  return direct_to_template(request, 'story/test.html', locals())