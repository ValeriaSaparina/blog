from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from records.forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import User, Post


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
    return render(request, 'records/author.html')


def u_edit():
    return None


def index():
    return None

# # Вариант регистрации на базе класса FormView
# class MyRegisterFormView(FormView):
#     # Указажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
#     # это UserCreationForm - стандартный класс Django унаследованный
#     form_class = UserCreationForm
#
#     # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
#     # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
#     success_url = "/login/"
#
#     # Шаблон, который будет использоваться при отображении представления.
#     template_name = "records/sign in.html"
#
#     def form_valid(self, form):
#         form.save()
#         print("Success")
#         # Функция super( тип [ , объект или тип ] )
#         # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
#         return super(MyRegisterFormView, self).form_valid(form)
#
#     def form_invalid(self, form):
#         print("Don't success")
#         return super(MyRegisterFormView, self).form_invalid(form)
