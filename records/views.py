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
        print(len(posts_list)-p.id + 1)
        posts.append(Post.objects.get(pk=len(posts_list)-p.id+1))
    s_list = []
    for p in posts_list:
        a = Post.objects.get(pk=len(posts_list)-p.id+1)
        s = a.text
        s = s[:444] + '...'
        s_list.append(s)
        print(s)
    for p in posts:
        print(p.title)
    print(type(posts_list))
    data = zip(posts, s_list)
    context = {'data': data, 'author': author, 'posts_list': posts_list}
    return render(request, 'records/main.html', context)


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('HEY')
            username = form.cleaned_data.get('username')
            # my_password = form.cleaned_data.get('password1')
            # email = form.cleaned_data.get('email')
            # user = User.objects.create_user(username=username,
            #                                 email=email,
            #                                 password=my_password)
            user = form.save()
            u_id = request.user.id
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # user = User.objects.get(pk=u_id)
            print('fuck', u_id)

            profile = Profile(user=user, nickname=username, count_posts=0, about=' ')
            profile.save()
        else:
            print("FUCK")
        return redirect('/')
    else:
        form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})


def p_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    print(post)
    profile_id = post.profile_id.id
    print(profile_id)
    author = get_object_or_404(Profile, pk=profile_id)
    print(author.id)
    return render(request, 'records/post_details.html', {'post': post, 'author': author})


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
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
        flag = False
    user_id = int(username)
    print('user_id: ', user_id)
    s_list = []
    posts_list = Post.objects.filter(profile_id=user_id)
    for p in posts_list:
        print('len post_list: ', len(posts_list))
        print('id: ', p.id)
        print('len: ', len(posts_list)-p.id+1)
        # a = Post.objects.get(pk=len(posts_list)-p.id+1) TODO: проверь эту большую фиговину
        s = p.text
        s = s[:444] + '...'
        s_list.append(s)
    info = Profile.objects.get(pk=user_id)
    data = zip(posts_list, s_list)
    return render(request, 'records/author.html', {'info': info, 'flag': flag, 'user_id': user_id, 'data': data,
                  'posts_list': posts_list})


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
