from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Post , City
from .forms import ProfileForm , PostForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def edit_profile(request,profile_id):
    pass

def about(request):
    pass

@login_required
def profile(request):#also known as profile index
    profile = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(profile=profile)
    context = {'profile': profile, 'posts':posts}
    return render(request,'profile/index.html', context)

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    # city= post.city
    context = {'post':post}
    # print(city)
    return render(request,'posts/detail.html', context)

@login_required
def add_post(request):
    error_message = ''
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        print(post_form.errors)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.profile = Profile.objects.get(user = request.user)
            new_post.save()
            return redirect('profile')
        else:
            error_message = post_form.errors
    context = {"post_form":PostForm(), 'error_message':error_message}
    return render(request,"posts/new.html",context)

@login_required
def city_detail(request, city_id):
    posts = Post.objects.filter(city=city_id)
    city = City.objects.get(id= city_id)
    print(len(posts))
    context = {'city':city, 'posts': posts}
    return render(request,'cities/detail.html', context)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(request.POST.get('name'))
        if form.is_valid():
            user = form.save()
            login(request,user)
            new_profile = Profile(name = request.POST.get('name'), user = user)
            new_profile.save()
            return redirect('profile')
        else:
            error_message = 'Invalid Sign Up - try again'
    
    form = UserCreationForm()
    profile_form  = ProfileForm()
    context = {
        'profile_form': profile_form,
        'form': form,
        'error_message': error_message
    }
    return render(request,'registration/signup.html', context)