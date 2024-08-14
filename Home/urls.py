from django.urls import path  
from .views import home,contact,blog,category,about,author,details_blog

urlpatterns = [
    path('',home,name='index'),
    path('contact/',contact,name='contact'),
    path('blog/',blog,name='blog'),
    path('details-blog/<int:post_id>/',details_blog,name='details_blog'),
    path('category/<int:category_id>/',category,name='category_details'),
    path('about/',about,name='about'),
    path('author/',author,name='author'), 
 #   path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
  #  path('comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),
]
