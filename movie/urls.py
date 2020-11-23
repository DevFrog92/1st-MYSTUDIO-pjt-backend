from django.urls import path
from . import views
app_name = 'movie'

urlpatterns = [
    path('',views.movielist,name='movielist'),
    path('create/',views.createroadmap,name='createroadmap'),
    path('watch/',views.watch,name='watch'),
    path('recommend/',views.recommend,name='recommend')
]
