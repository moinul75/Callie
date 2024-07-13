from django.db import models 
from django.contrib.auth.models import User 
from django.utils.text import slugify 
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

# Create your models here. 
class Category(models.Model): 
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='category/',null=True,blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    
    def __str__(self) -> str:
        return self.name  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Post(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) 
    tags = TaggableManager() 
    
    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) 
        

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for {self.post.title}"
    



    
    
    
                       
