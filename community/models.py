from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Review(models.Model):
    movie_title = models.CharField(max_length=50)
    rank = models.IntegerField(default=1)
    content = models.TextField()
    poster_path = models.TextField(blank=True)
    movie_id = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='reviews')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100,blank=True)
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
