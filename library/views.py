from django.shortcuts import get_object_or_404, render

from .models import Story


def _split_story_into_pages(content, max_page_length=500):
    pages = []
    current_page = ''
    for paragraph in content.splitlines():
        words = paragraph.split()
        for word in words:
            if current_page and len(current_page) + len(word) + 1 > max_page_length:
                pages.append(current_page)
                current_page = ''
            current_page = '{} {}'.format(current_page, word).strip()
        if current_page:
            pages.append(current_page)
            current_page = ''
    if current_page:
        pages.append(current_page)
    return pages


def _build_book_pages(story_pages):
    book_pages = []
    for story_page in story_pages:
        image = story_page.get('image') if isinstance(story_page, dict) else story_page.image
        text = story_page.get('text', '') if isinstance(story_page, dict) else story_page.text
        if image:
            book_pages.append({
                'kind': 'illustration',
                'image': image,
                'page_number': len(book_pages) + 1,
            })
        if text.strip():
            book_pages.append({
                'kind': 'text',
                'text': text,
                'page_number': len(book_pages) + 1,
            })
    if not book_pages:
        book_pages.append({
            'kind': 'text',
            'text': 'This story does not have any pages yet.',
            'page_number': 1,
        })
    return book_pages


def home(request):
    selected_category = request.GET.get('category', 'all')

    stories = Story.objects.all()

    print("TOTAL STORIES IN DATABASE:", Story.objects.count())
    print("STORIES SENT TO HOME:", stories.count())
    print("SELECTED CATEGORY:", selected_category)

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
    pages = list(story.pages.all())
    if not pages:
        pages = [
            {'text': text}
            for page_number, text in enumerate(_split_story_into_pages(story.content), start=1)
        ]
    return render(request, 'library/story_detail.html', {
        'story': story,
        'book_pages': _build_book_pages(pages),
    })
