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
