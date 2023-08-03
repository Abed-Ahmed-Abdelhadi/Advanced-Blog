from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('tag/<slug:tag_slug>/', views.blog_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.blog_detail, name='blog_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/comment/',views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]