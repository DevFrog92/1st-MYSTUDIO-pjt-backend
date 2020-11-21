from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StudioGhibli
from .serializers import StudioGhibliSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.status import HTTP_201_CREATED
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