from rest_framework import serializers
from .models import Review,Profile,Comment
# from ..accounts.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','movie_title','rank','content','poster_path','movie_id','created_at','updated_at','username')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','content','username','created_at','updated_at')