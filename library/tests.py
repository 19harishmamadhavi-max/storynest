from django.test import TestCase

from .models import Story


class StoryPageTests(TestCase):
    def setUp(self):
        self.story = Story.objects.create(
            title='The Moonlit Meadow',
            author='A. Storyteller',
            age_group='6-7',
            category='fiction',
            content='Milo the mouse found a tiny silver star.',
        )

    def test_home_page_lists_stories(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Moonlit Meadow')
        self.assertContains(response, 'A. Storyteller')
        self.assertContains(response, 'Fiction and Fantasy')

    def test_home_page_filters_stories_by_category(self):
        moral_story = Story.objects.create(
            title='A Kind Little Seed',
            author='A. Storyteller',
            age_group='4-5',
            category='moral',
            content='A seed shared its shade with a tiny bug.',
        )
        response = self.client.get('/?category=moral')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, moral_story.title)
        self.assertNotContains(response, 'The Moonlit Meadow')

    def test_story_page_shows_story_content(self):
        response = self.client.get('/stories/{}/'.format(self.story.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milo the mouse')
        self.assertContains(response, 'Ages 6-7')

    def test_missing_story_returns_not_found(self):
        response = self.client.get('/stories/99999/')

        self.assertEqual(response.status_code, 404)
