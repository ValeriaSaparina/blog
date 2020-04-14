from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.utils import timezone

from .forms import AuthorForm
from .forms import NewPostForm
from .models import User, Post, Profile


def users(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'records/users.html', context)


def main(request):
    posts_list = Post.objects.all()
    s_list = []
    for p in posts_list:
        s = p.text
        s = s[:2] + '...'
        s_list.append(s)
        print(p.id)
        print(s_list[p.id-1])
    print(type(posts_list))
    data = zip(posts_list, s_list)
    context = {'data': data}
    return render(request, 'records/main.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        username = form.cleaned_data.get('username')
        my_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=my_password)
        login(request, user)
        return redirect('/')
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


def p_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    print(post)
    profile_id = post.profile_id.id
    print(profile_id)
    author = Profile.objects.get(pk=profile_id)
    return render(request, 'records/post_details.html', {'post': post, 'author': author})


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            p = form.save()
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        # theme = form.cleaned_data.get('theme')
        theme = "test"
        pub_date = timezone.now()
        profile = Profile.objects.get(pk=request.user.id)
        profile.count_posts = profile.count_posts + 1
        profile.save()
        profile_id = request.user.id
        author = profile.nickname
        likes = 0
        print(title, text, author, pub_date, profile_id, likes, theme)
        profile.post_set.create(title=title, text=text, theme=theme, pub_date=pub_date, author=author, likes=likes)
        post = Post.objects.all()
        length = len(post)
        return redirect('/posts/' + str(length))
    else:
        form = NewPostForm()
        print("jjj")
        return render(request, 'records/new_post.html', {'form': form})


def u_details(request, username):
    user_id = request.user.id
    if user_id == int(username):
        flag = True
    else:
        user_id = int(username)
        flag = False
    info = Profile.objects.get(pk=user_id)
    return render(request, 'records/author.html', {'info': info, 'flag': flag, 'user_id': user_id})


def edit(request):
    info = Profile.objects.get(pk=request.user.id)
    print(request.method)
    if request.method == 'POST':
        print("HELLO FRIEND")
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
        nickname = form.cleaned_data.get('nickname')
        about = form.cleaned_data.get('about')
        profile = Profile.objects.get(pk=request.user.id)
        profile.nickname = nickname
        profile.about = about
        print(about, profile)
        profile.save()
        flag = True
        return render(request, 'records/author.html', {'flag': flag, 'info': profile})
    else:
        form = AuthorForm()
        print('else')
        return render(request, 'records/author_edit.html', {'info': info})
