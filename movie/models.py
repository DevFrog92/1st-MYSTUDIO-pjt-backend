from django.db import models
from django.conf import settings
# Create your models here.

class StudioGhibli(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='roadmap')
    spiritedaway = models.BooleanField(default=False)
    princessmononoke = models.BooleanField(default=False)
    Kikisdeliveryservice = models.BooleanField(default=False)
    myneighbortotoro = models.BooleanField(default=False)
    howlsmovingcastle = models.BooleanField(default=False)


class FavoriteMovie(models.Model):
    favorite_user = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='favorite_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='favorite')
    movie_title = models.CharField(max_length=50)
    poster_path = models.TextField(blank=True)
    movie_id = models.CharField(max_length=100,blank=True)
    overview = models.TextField(blank=True)
    genre = models.CharField(max_length=100,blank=True)

