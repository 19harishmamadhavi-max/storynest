from django.test import TestCase

from .models import Story, StoryPage


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

    def test_home_page_has_storybook_splash_and_lazy_cover_art(self):
        response = self.client.get('/')

        self.assertContains(response, 'Start Reading')
        self.assertNotContains(response, 'Skip')
        self.assertContains(response, 'images/splash.jpg.jpg')
        self.assertContains(response, 'images/hero.jpg.jpg')
        self.assertContains(response, 'images/cover-moral.jpg.jpg')
        self.assertContains(response, 'loading="lazy"')

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
        self.assertContains(response, 'Page 1')

    def test_story_without_pages_splits_content_into_passages(self):
        self.story.content = (
            'The race began.\r\n'
            'The hare took a nap while the tortoise kept going.\r\n'
            'Slow and steady won.'
        )
        self.story.save()

        response = self.client.get('/stories/{}/'.format(self.story.pk))
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertLess(content.index('Page 1'), content.index('The race began.'))
        self.assertLess(content.index('Page 2'), content.index('The hare took a nap'))
        self.assertLess(content.index('Page 3'), content.index('Slow and steady won.'))

    def test_story_pages_are_displayed_in_page_number_order(self):
        StoryPage.objects.create(
            story=self.story,
            page_number=2,
            text='The mouse went home.',
        )
        StoryPage.objects.create(
            story=self.story,
            page_number=1,
            text='The mouse found a star.',
        )

        response = self.client.get('/stories/{}/'.format(self.story.pk))
        content = response.content.decode()

        self.assertLess(content.index('The mouse found a star.'), content.index('The mouse went home.'))
        self.assertNotContains(response, 'Milo the mouse')

    def test_missing_story_returns_not_found(self):
        response = self.client.get('/stories/99999/')

        self.assertEqual(response.status_code, 404)
