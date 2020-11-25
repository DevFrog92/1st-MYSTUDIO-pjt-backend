from django.urls import path
from . import views
app_name = 'movie'

urlpatterns = [
    path('',views.movielist,name='movielist'),
    path('create/',views.createroadmap,name='createroadmap'),
    path('watch/',views.watch,name='watch'),
    path('recommend/',views.recommend,name='recommend'),
    path('<int:movie_id>/favorite_read_save/',views.favorite_read_save,name='favorite_read_save'),
    path('<int:movie_id>/favorite_state/',views.favorite_state,name='favorite_state'),
]
