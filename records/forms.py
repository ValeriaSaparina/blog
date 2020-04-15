from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from records.models import Post


class SignInFrom(forms.Form):
    email = forms.CharField(label='Your email', max_length=100)
    password = forms.CharField(label='Your password', max_length=100)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class AuthorForm(forms.Form):
    nickname = forms.CharField(label="nickname", max_length=20)
    count_posts = forms.IntegerField(label="count_posts")
    about = forms.CharField(label="about", max_length=500)


class NewPostForm(ModelForm):
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=2000, widget=forms.Textarea)
    theme = forms.CharField(max_length=30)

    class Meta:
        model = Post
        fields = ['profile_id', 'title', 'text', 'author', 'theme', 'pub_date', 'likes']
