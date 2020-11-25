from rest_framework import serializers
from .models import StudioGhibli,FavoriteMovie


class StudioGhibliSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioGhibli
        fields = '__all__'

class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ('id','movie_title','genre','overview','poster_path','movie_id',)