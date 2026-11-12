from django.shortcuts import get_object_or_404, render

from .models import Story


def home(request):
    stories = Story.objects.all().order_by('title')
    return render(request, 'library/home.html', {'stories': stories})


def story_detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    return render(request, 'library/story_detail.html', {'story': story})
