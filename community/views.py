from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Review, Comment,Profile
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_403_FORBIDDEN
from .serializers import ReviewSerializer,ProfileSerializer,CommentSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
import random 

profile_imgages = [

    '/profile/ogu.jpg',
    '/profile/marvel.png',
    '/profile/totoro.png',
    '/profile/tube.png',
    '/profile/zordy.png'
]


@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        if Profile.objects.filter(user_id = request.user.pk):
            profile = get_object_or_404(Profile,user_id = request.user.pk)          
            profile.username = request.user.username
            profile.save()
            return Response({'message':'이미존재합니다'})
        else:
            profile = Profile.objects.create(user=request.user)
            index = random.sample(profile_imgages,1)
            profile.img = str(index[0])
            profile.username = request.user.username
            profile.save()
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
    else:
        profile = get_object_or_404(Profile,user_id = request.user.pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def updateprofile(request):
    profile = get_object_or_404(Profile,user_id = request.user.pk)
    profile.description = request.data.get('description')
    profile.nickname = request.data.get('nickname')
    profile.genre = request.data.get('genre')
    profile.best_movie_title_1 = request.data.get('best_movie_title_1')
    profile.best_movie_id_1 = request.data.get('best_movie_id_1')
    profile.best_movie_title_2 = request.data.get('best_movie_title_2')
    profile.best_movie_id_2 = request.data.get('best_movie_id_2')
    profile.best_movie_title_3 = request.data.get('best_movie_title_3')
    profile.best_movie_id_3 = request.data.get('best_movie_id_3')
    profile.save()
    return Response('response data')

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def analyze_image(request):
    # print(request.FILES)
    # src = request.FILES['files'] # 파일이 하나일 경우
    #for img in request.FILES.getlist('files'):   # 파일이 여러개일 경우
    #    upload_img = UploadImage.objects.create(image=img, .....)
    serializer = ReviewSerializer(data=request.data)
    print(request.data)
    print(serializer)
    print(serializer.is_valid())
    ########
    # ########
    # uploaded_image = HairImage.objects.create(upload_image=src, upload_user=request.user)
	# ########
    # ########
    return Response('response할 내용')

#################################
@api_view(['GET'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def index(request):
    print('들어왔어')
    reviews = Review.objects.order_by('-pk')
    serializer = ReviewSerializer(reviews,many=True)
    print(serializer.data)
    context = {
        'reviews': reviews,
    }
    return Response(serializer.data,status=HTTP_200_OK)
    # return render(request,'community/index.html',context)


@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_read_create(request):
    '''
    Todo List 조회 및 Todo를 생성하는 함수입니다.
    '''
    if request.method == 'GET':
        # 1. 작성자에 따른 글을 가지고 온다.
        print(request.user)
        # reviews_list = request.user.reviews
        reviews_list = Review.objects.order_by('-pk')
        # todo_list = Todo.objects.filter(user = request.user)
        serializer = ReviewSerializer(reviews_list,many=True)
        return Response(serializer.data)
    else:
        serializer = ReviewSerializer(data=request.data)
        print(request.user,request.data)
        if serializer.is_valid(raise_exception=True):
            print('저장한다.')
            serializer.save(user=request.user,username=request.user.username)
            return Response(serializer.data,status=HTTP_201_CREATED)




@api_view(['PUT','DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_update_delete(request,review_id):
    print('함수들어간다')
    '''
    Todo를 수정 혹은 삭제하는 함수입니다.
    '''
    review = get_object_or_404(Review,pk=review_id)

    if review.user != request.user:
        return Response({'detail':'권한이 없습니다.'},status=HTTP_403_FORBIDDEN)
    print('일단 지나간다',request.method)
    if request.method =='PUT':
        print('변환한다',request,review)
        serializer = ReviewSerializer(review,data=request.data)
        if serializer.is_valid(raise_exception=True):
            print('저장한다')
            serializer.save()
            return Response(serializer.data)
    else:
        review.delete()
        return Response({'message':'안녕'})









# @login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        print(request.user)
        print(request.POST,request.FILES)
        form = ReviewForm(request.POST,request.FILES) 
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)
@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    # 없는 pk로 접근했을때 404
    review = get_object_or_404(Review, pk=review_pk)
    # 없는 pk로 접근했을때 500
    # article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('community:detail', review_pk)
    else: 
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'community/update.html', context)

@require_POST
def delete(request, review_pk):
    if request.user.is_authenticated:
        article = Review.objects.get(pk=review_pk)
        article.delete()
    return redirect('community:index')

@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)




@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def read_create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    print(review_pk)
    if request.method == 'GET':
        comments = review.comment_set.all()
        print(comments)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)
    else:
        print('들어ㅏ왔다잉',request.data)
        serializer = CommentSerializer(data=request.data)
        print('생성한다')
        if serializer.is_valid(raise_exception=True):
            print('검사한다잉')
            serializer.save(user = request.user,username=request.user.username,review=review)
            return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def read_create_comment(request, review_pk):
#     review = get_object_or_404(Review, pk=review_pk)
#     print(review_pk)
#     if request.method == 'GET':
#         comments = review.comment_set.all()
#         print(comments)
#         serializer = CommentSerializer(comments,many=True)
#         return Response(serializer.data)
#     else:
#         print('들어ㅏ왔다잉',request.data)
#         serializer = CommentSerializer(data=request.data)
#         print('생성한다')
#         if serializer.is_valid(raise_exception=True):
#             print('검사한다잉')
#             serializer.save(user = request.user,username=request.user.username,review=review)
#             return Response(serializer.data)





@api_view(['DELETE','PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_update_comment(request,comment_pk):
    res_user = request.user
    comment = get_object_or_404(Comment,pk=comment_pk)
    print(res_user.id, comment.user_id) 
    if res_user.id == comment.user_id:
        if request.method == 'DELETE':
            print(comment)
            comment.delete()
            return Response({'message':'delete'})
        else:
            serializer = CommentSerializer(comment,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user = request.user,username=request.user.username)
                return Response(serializer.data)
    else:
        return Response({'message':'404'})







@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like(request,review_pk):
    print('들어온다',request.user.pk)
    review = get_object_or_404(Review,pk=review_pk)
    print('있다',review)
    user = request.user
    if request.method=='GET':
        if review.like_users.filter(pk=user.pk).exists():
            liked = True
            count = review.like_users.count()
        else:
            liked = False
            count = review.like_users.count()
        return Response({'count':count,'liked':liked})
    else:
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False
            count = review.like_users.count()
        else:
            review.like_users.add(user)
            liked = True
            count = review.like_users.count()
        context = {
            'liked':liked,
            'count':count,
        }
        return JsonResponse(context)



