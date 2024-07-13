from django.urls import path  
from .views import home,contact,blog,category,about,author,details_blog

urlpatterns = [
    path('',home,name='index'),
    path('contact/',contact,name='contact'),
    path('blog/',blog,name='blog'),
    path('details-blog/<int:post_id>/',details_blog,name='details_blog'),
    path('category/',category,name='category'),
    path('about/',about,name='about'),
    path('author/',author,name='author'),
]
