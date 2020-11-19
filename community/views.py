from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from .serializers import ReviewSerializer




@api_view(['POST'])
def analyze_image(request):
    # print(request.FILES)
    # src = request.FILES['files'] # 파일이 하나일 경우
    #for img in request.FILES.getlist('files'):   # 파일이 여러개일 경우
    #    upload_img = UploadImage.objects.create(image=img, .....)
    serializer = ReviewSerializer(data=request.data)
    print(request.data)
    print(serializer.is_valid())
    ########
    # ########
    # uploaded_image = HairImage.objects.create(upload_image=src, upload_user=request.user)
	# ########
    # ########
    return Response('response할 내용')

#################################

@api_view(['GET'])
def index(request):
    reviews = Review.objects.order_by('-pk')
    serializer = ReviewSerializer(reviews,many=True)
    print(serializer.data)
    context = {
        'reviews': reviews,
    }
    return Response(serializer.data,status=HTTP_200_OK)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES) 
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


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def like(request,review_pk):
    review = get_object_or_404(Review,pk=review_pk)
    if request.user.is_authenticated:
        user = request.user
        auth_user = True
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False
            count = review.like_users.count()
        else:
            review.like_users.add(user)
            liked = True
            count = review.like_users.count()
    else:
        auth_user = False
        liked = False
        count = review.like_users.count()
    context = {
        'liked':liked,
        'count':count,
        'auth_user':auth_user,
    }
    return JsonResponse(context)