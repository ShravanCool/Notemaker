"""Notemaker URL Configuration

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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import routers
from .views import UserCreateView, LoginIndexView, LogOut, UserViewSet
from Notes.views import (NotesListDashboard, TermViewSet, CourseViewSet,
                         ClassNoteViewSet,)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'terms', TermViewSet, basename='term')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'classnotes', ClassNoteViewSet, basename='classnote')

urlpatterns = [
    path(
        'admin/',
         admin.site.urls,
         name = 'admin',
         ),
    path(
        'Dashboard/',
         login_required(NotesListDashboard.as_view()),
         name = 'dashboard',
        ),
    path(
        '',
        LoginIndexView.as_view(),
        name = 'loginindex',
        ),
    path(
        'Logout/',
         login_required(LogOut.as_view()),
         name = 'logout',
         ),
    path(
        'Register/',
        UserCreateView.as_view(),
        name = 'register',
        ),
    path(
        'Notes/',
         include('Notes.urls'),
        ),
    path(
        'Web-API/',
        include(router.urls),
        ),
    path(
        'API-auth/',
        include('rest_framework.urls'),
        name = 'rest_framework',
        ),
]
