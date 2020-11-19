from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm,CustomUserChangeForm,ProfileForm
from .models import Profile
from django.http import JsonResponse

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            
            auth_login(request, user)
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('community:index')


@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('community:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request,'accounts/update.html',context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        reqeust.user.delete()
    return redirect('community:index')


@login_required
@require_http_methods(['GET','POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return redirect('community:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form
    }
    return render(request,'accounts/change_password.html',context)

@login_required
def profile(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    print(person.profile.img)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request,user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(),pk=user_pk)
        me = request.user
        if me != person:
            if person.followings.filter(pk=me.pk).exists():
                print('언팔한다',me.pk)
                person.followings.remove(me)
                folloewd = False
                followers_count = person.followers.count()
                followings_count = person.followings.count()
            else:
                print('팔한다')
                person.followings.add(me)
                folloewd = True
                followers_count = person.followers.count()
                followings_count = person.followings.count()
            
            context  = {
                'followed':folloewd,
                'follower_count':followers_count,
                'following_count':followings_count,
            }
            return JsonResponse(context)
    return redirect('accounts:profile',person.username)


@login_required
@require_http_methods(['GET','POST'])
def update_profile(request,user_id):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:profile',user_id)
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form':form
    }
    return render(request,'accounts/profile_update.html',context)

