from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from story.forms import StoryForm, TestImageForm
from story.models import Story as StoryModel
from story.models import StoryImage, TestImage

@login_required
def add_story(request):
  if request.method == 'POST':
    form = StoryForm(request.POST, request.FILES)

    if form.is_valid():
      story = form.save(commit=False)
      story.user = request.user
      story.save()

      if form.cleaned_data['images']:
        for image in form.cleaned_data['images']:
          saved_image = StoryImage.objects.create(image=image)
          story.images.add(saved_image)
      
      story.save()
      return render_to_response('success.html')
  else:
      form = StoryForm()
  return direct_to_template(request, 'story/add.html', locals())

def test_image(request):
  if request.method == 'POST':
    form = TestImageForm(request.POST, request.FILES)
    
    if form.is_valid():
      form.save()
      return render_to_response('success.html')
  else:
    form = TestImageForm()
  return direct_to_template(request, 'story/test.html', locals())
