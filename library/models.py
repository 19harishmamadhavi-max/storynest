from django.db import models


class Story(models.Model):
    AGE_GROUP_CHOICES = [
        ('4-5', 'Ages 4-5'),
        ('6-7', 'Ages 6-7'),
        ('8-10', 'Ages 8-10'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    age_group = models.CharField(max_length=5, choices=AGE_GROUP_CHOICES)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='story_covers/')

    def __str__(self):
        return self.title
