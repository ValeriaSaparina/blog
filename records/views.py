from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.utils import timezone

# from .forms import AuthorForm
from .forms import NewPostForm
from .models import User, Post, Profile


def users(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'records/users.html', context)


def main(request):
    posts_list = Post.objects.all()
    context = {'posts_list': posts_list, }
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


def p_details():
    return None


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        # theme = form.cleaned_data.get('theme'
        theme = "test"
        pub_date = timezone.now()
        profile = Profile.objects.get(pk=request.user.id)
        profile_id = request.user.id
        author = profile.nickname
        likes = 0
        print(title, text, author, pub_date, profile_id, likes, theme)
        profile.post_set.create(title=title, text=text, theme=theme, pub_date=pub_date, author=author, likes=likes)
        return render(request, 'records/post_details.html')
    else:
        form = NewPostForm()
        return render(request, 'records/new_post.html', {'form': form})


def u_details(request, username):
    user_id = request.user.id
    info = Profile.objects.get(pk=user_id)
    print(info)
    return render(request, 'records/author.html', {'info': info})


def u_edit(request, username):
    # if request.method == 'POST':
    #     form = AuthorForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     nickname = form.cleaned_data.get('nickname')
    #     about = form.cleaned_data.get('about')
    #     a = Profile(nickname=nickname, about=about)
    #     a.save()
    #     print(a.nickname)
    # else:
    #     form = AuthorForm()

    return render(request, 'records/author_edit.html')
