from django.shortcuts import get_object_or_404, render

from .models import Story


def home(request):
    selected_category = request.GET.get('category', 'all')
    stories = Story.objects.all()
    if selected_category in dict(Story.CATEGORY_CHOICES):
        stories = stories.filter(category=selected_category)
    else:
        selected_category = 'all'
    return render(request, 'library/home.html', {
        'stories': stories.order_by('title'),
        'categories': Story.CATEGORY_CHOICES,
        'selected_category': selected_category,
    })


def story_detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    return render(request, 'library/story_detail.html', {'story': story})
