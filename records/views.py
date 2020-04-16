from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import AuthorForm, RegistrationForm
from .forms import NewPostForm
from .models import User, Post, Profile


def users(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'records/users.html', context)


def main(request):
    author = Profile.objects.all()
    posts_list = Post.objects.all()
    posts = []
    for p in posts_list:
        posts.append(Post.objects.get(pk=len(posts_list)-p.id+1))
    s_list = []
    for p in posts_list:
        a = Post.objects.get(pk=len(posts_list)-p.id+1)
        s = a.text
        s = s[:444] + '...'
        s_list.append(s)
    data = zip(posts, s_list)
    context = {'data': data, 'author': author, 'posts_list': posts_list}
    return render(request, 'records/main.html', context)


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            profile = Profile(user=user, nickname=username, count_posts=0, about=' ')
            profile.save()
        else:
            flag = True
            form = RegistrationForm()
            return render(request, 'registration/signup.html', {'flag': flag, 'form': form})
        return redirect('/')
    else:
        form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})


def p_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    profile_id = post.profile_id.id
    author = get_object_or_404(Profile, pk=profile_id)
    if profile_id == request.user.id:
        flag = True
    else:
        flag = False
    return render(request, 'records/post_details.html', {'post': post, 'author': author, 'flag': flag})


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        theme = "test"
        pub_date = timezone.now()
        profile = Profile.objects.get(pk=request.user.id)
        profile.count_posts = profile.count_posts + 1
        profile.save()
        author = profile.nickname
        likes = 0
        profile.post_set.create(title=title, text=text, theme=theme, pub_date=pub_date, author=author, likes=likes)
        post = Post.objects.all()
        length = len(post)
        return redirect('/posts/' + str(length))
    else:
        form = NewPostForm()
        return render(request, 'records/new_post.html', {'form': form})


def u_details(request, username):
    user_id = request.user.id
    if user_id == int(username):
        flag = True
    else:
        flag = False
    user_id = int(username)
    s_list = []
    posts_list = Post.objects.filter(profile_id=user_id)
    for p in posts_list:
        s = p.text
        s = s[:444] + '...'
        s_list.append(s)
    info = Profile.objects.get(pk=user_id)
    print(info.about)
    data = zip(posts_list, s_list)
    return render(request, 'records/author.html', {'info': info, 'flag': flag, 'user_id': user_id, 'data': data,
                  'posts_list': posts_list})


def edit(request):
    info = Profile.objects.get(pk=request.user.id)
    print(request.method)
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
        nickname = form.cleaned_data.get('nickname')
        about = form.cleaned_data.get('about')
        profile = Profile.objects.get(pk=request.user.id)
        user = User.objects.get(pk=request.user.id)
        user.username = nickname
        user.save()
        profile.nickname = nickname
        profile.about = about
        profile.save()
        flag = True
        return render(request, 'records/author.html', {'flag': flag, 'info': profile})
    else:
        form = AuthorForm()
        return render(request, 'records/author_edit.html', {'info': info})
