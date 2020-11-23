from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StudioGhibli
from .serializers import StudioGhibliSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.status import HTTP_201_CREATED

import os
import sys
import urllib.request
import requests
from urllib.parse import urlparse
import datetime

# Create your views here.

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movielist(request):
    user = request.user
    if StudioGhibli.objects.filter(user_id = user.pk):
        ghibri = StudioGhibli.objects.get(user_id = user.pk)
        serializer = StudioGhibliSerializer(ghibri)
        print(serializer)
        return Response({'url':'http://127.0.0.1:8000/api/Ghibli/ghibli.png','data':serializer.data})
    else:
        return Response({'url':''})


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def createroadmap(request):
    user = request.user
    print('들어왔어',user.pk)
    # roadmap = get_object_or_404(StudioGhibli,user_id=request.user.pk)
    if StudioGhibli.objects.filter(user_id = user.pk):
        return Response({'messgae':'이미 생성되었습니다.'})
    else:
        StudioGhibli.objects.create(user = user)
        print('객체생성 성공')
        return Response({'message':'성공적으로 생성되었습니다.'},status=HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def watch(request):
    user = request.user
    print('dldldldldldldl')
    print(request.data.get('howlsmovingcastle'))
    ghibri = StudioGhibli.objects.get(user_id = user.pk)
    ghibri.howlsmovingcastle = request.data.get('howlsmovingcastle')
    ghibri.save()
    print(ghibri.howlsmovingcastle)
    return Response({'message':'안돼'})


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend(request):
    genre_id = {'drama':18,'fantasy':14,'horror':27,'romance':10749,'adventure':12,'thriller':53,
    'comedy':35,'mystery':9648,'war':10752,'action':28,'sf':878,'animation':16,'crime':80,'documentary':99,
    'family':10751,'history':36,'music':10402}
    print('요청이다',request.data)
    keyword = {}
    tmp = list(map(int,request.data.get('genre').split(',')))
    temp = {}
    genre_name =[]
    for idx in tmp:
        for key,value in genre_id.items():
            if value == idx:
                temp[key] = []
                genre_name.append(key)

    for i in range(1,3):
        key = 'e37c0ae71977e8ad20b5a3f6caa339a1'
        url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={key}&language=ko-KR&page={i}"
        print(url)
        result = requests.get(urlparse(url).geturl())
        response = result.json()
        print(response)

        for item in response['results']:
            print(item)
            for idx in item['genre_ids']:
                if idx in tmp:
                    for key,value in genre_id.items():
                        if value == idx and item not in temp[key]:
                            temp[key].append(item)
        print(temp)
    return Response({'data':temp,'data2':genre_name})