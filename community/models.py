from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Review(models.Model):
    title = models.CharField(max_length=100)
    movie_title = models.CharField(max_length=50)
    rank = models.IntegerField()
    content = models.TextField()
    # img = ProcessedImageField(
    #     blank = True,
    #     upload_to = '%Y/%m/%d/',
    #     processors=[
    #         Thumbnail(width=500)
    #     ],
    #     format='JPEG'
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='reviews')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')


class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Profile(models.Model):
    # user model 1:1
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40,blank=True)
    genre = models.CharField(max_length=100,blank=True)
    best_movie_title = models.CharField(max_length=50,blank=True)
    best_movie_id = models.CharField(max_length=100,blank=True)
    username = models.CharField(max_length=100,blank=True)
    img = ProcessedImageField(
        blank = True,
        upload_to = 'profile/images',
        processors=[
           ResizeToFill(300, 300)
        ],
        format='JPEG',
        options = {'quality':90},
    )
