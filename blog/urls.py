from django.urls import path

from .views import blog, post_detail, search, tag_search, category_search, upload

app_name = 'blog'

urlpatterns = [
    path('', blog, name='home'),
    path('post/<pk>/', post_detail, name='post-detail'),
    path('search/', search, name='search'),
    path('tag/<str:name>', tag_search, name='tag_search'),
    path('category/<str:name>', category_search, name='category_search'),
    path('upload/', upload, name='upload'),
]
