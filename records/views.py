from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# from .forms import AuthorForm
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


def index():
    return None