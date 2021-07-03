
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    PostListView,
    PostDetailView,
    # PostCreateView,
    # PostUpdateView,
    # PostDeleteView
)

urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('about/', views.about, name='blog-about'),
]
