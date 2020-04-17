from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import AuthorForm, RegistrationForm, PostEditForm
from .forms import NewPostForm
from .models import User, Post, Profile


def get_my_fav(user_id):
    user = Profile.objects.get(pk=user_id)
    fav = user.my_favorites
    fav_users = fav.split(';')
    return fav_users


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
            profile = Profile(user=user, nickname=username, count_posts=0, about='', my_favorites='', count_favorites=0)
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
    if request.method == "POST":
        post.likes = post.likes + 1
        post.save()
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
    data = zip(posts_list, s_list)
    if request.method == 'POST':
        user = Profile.objects.get(pk=user_id)
        my_profile = Profile.objects.get(pk=request.user.id)
        my_fav = get_my_fav(request.user.id)
        flag_fav = True
        for f in my_fav:
            if f == str(user_id):
                flag_fav = True
                break
            else:
                flag_fav = False
        if flag_fav:
            user.count_favorites = user.count_favorites - 1
            user.save()
            my_fav.remove(str(username))
            my_profile.my_favorites = ''.join(my_fav)
            my_profile.save()
        else:
            user.count_favorites = user.count_favorites + 1
            user.save()
            my_profile.my_favorites = my_profile.my_favorites + username + ';'
            my_profile.save()
    user_id = int(username)
    return render(request, 'records/author.html', {'info': info, 'flag': flag, 'user_id': user_id, 'data': data,
                  'posts_list': posts_list})


def edit(request):
    info = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
        nickname = form.cleaned_data.get('nickname')
        about = form.cleaned_data.get('about')
        if about is None:
            about = ""
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


def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PostEditForm(request.POST)
        if form.is_valid():
            form.save()
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        post.title = title
        post.text = text
        post.save()
        return redirect('/posts/' + str(post_id))
    else:
        form = PostEditForm()
        return render(request, 'records/post_edit.html', {'form': form, 'post': post})