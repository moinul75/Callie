from django.shortcuts import render,redirect ,get_object_or_404
from .models import Category,Post,PostImage 
from django.contrib import messages
from .forms import NewslatterForm

def get_category(): 
    category = Category.objects.all() 
    category_dict = {} 
    
    for category in category: 
        if  category.parent is None: 
            category_dict[category] = [] 
        if category.parent in category_dict: 
            category_dict[category.parent].append(category) 
    return category_dict
    
        

def home(request): 
    if request.method == 'POST':
        form = NewslatterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to the newsletter.')
            return redirect('index')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = NewslatterForm()
        
    hero_posts = {}
    categories = Category.objects.all()
    recent_posts = Post.objects.order_by('-created_at')[:4]
    lifestyle_posts = Post.objects.filter(category__name='Life Style')

    for category in categories:
        latest_post = Post.objects.filter(category=category).order_by('-created_at').first()
        if latest_post:
            hero_posts[category.name] = latest_post
    context = {
        'recent_posts': recent_posts,
        'lifestyle_posts': lifestyle_posts,
        'hero_posts': hero_posts, 
        'newslatter_form': form,
    }
    return render(request, 'index.html', context)

def contact(request):
    return render(request,'contact.html')  

def details_blog(request, post_id):  
    post = get_object_or_404(Post, id=post_id) 
    context = {
        'post':post
    }
    return render(request,'details_blog.html',context)

def blog(request): 
    return render(request,'blog-post.html')  

def category(request): 
    return  render(request,'category.html') 

def about(request): 
    return render(request,'about.html')   

def author(request): 
    return render(request, 'author.html')

