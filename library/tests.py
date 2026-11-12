from django.test import TestCase

from .models import Story


class StoryPageTests(TestCase):
    def setUp(self):
        self.story = Story.objects.create(
            title='The Moonlit Meadow',
            author='A. Storyteller',
            age_group='6-7',
            content='Milo the mouse found a tiny silver star.',
        )

    def test_home_page_lists_stories(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Moonlit Meadow')
        self.assertContains(response, 'A. Storyteller')

    def test_story_page_shows_story_content(self):
        response = self.client.get('/stories/{}/'.format(self.story.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milo the mouse')
        self.assertContains(response, 'Ages 6-7')

    def test_missing_story_returns_not_found(self):
        response = self.client.get('/stories/99999/')

        self.assertEqual(response.status_code, 404)
