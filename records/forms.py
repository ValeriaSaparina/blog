from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignInFrom(forms.Form):
    email = forms.CharField(label='Your email', max_length=100)
    password = forms.CharField(label='Your password', max_length=100)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class AuthorForm(forms.Form):
    nickname = forms.CharField(label="nickname", max_length=20, default="")
    count_posts = forms.IntegerField(label="count_posts", default=0)
    about = forms.CharField(label="about", max_length=500, default="")
