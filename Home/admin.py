from django.contrib import admin
from .models import Category, Post, PostImage, Comment, Reply
from tinymce.widgets import TinyMCE
from django.db import models

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    
class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    inlines = [ReplyInline]

class PostAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.TextField: {'widget': TinyMCE()},
    # }
    inlines = [PostImageInline, CommentInline]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
