# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('search/rank/', views.blog_search_rank, name='blog_search_rank'),
    path('search/similarity/', views.blog_search_similarity, name='blog_search_similarity'),
    path('<int:blog_id>/share/', views.share_blog, name='share_blog'),  
    path('<int:pk>/', views.blog_detail, name='blog_detail'),

]

