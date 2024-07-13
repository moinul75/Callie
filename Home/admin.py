from django.contrib import admin
from .models import Category, Post, PostImage
from tinymce.widgets import TinyMCE
from django.db import models

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.TextField: {'widget': TinyMCE()},
    # }
    inlines = [PostImageInline]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
