"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as vw

from records import views

app_name = 'records'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.main, name="main"),
    path('users/', views.users, name='users'),
    path('author/<str:username>', views.u_details, name='author'),
    path('posts/<str:post_id>', views.p_details, name='post'),
    path('edit', views.edit, name='edit'),
    path('posts/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('new_post/', views.new_post, name='new_post'),
    path('authors/fav/', views.fav, name='fav'),

    path('login/', vw.LoginView.as_view(), name='login'),
    path('reg/', views.signup, name='reg'),
    path('logout/', vw.LogoutView.as_view(), name='logout'),

]
