from Home.models import Category,Newslatter,Post,PostImage
from taggit.models import Tag 
from django.db.models import Count 
from .forms import NewslatterForm  
from django.contrib import messages 

def get_category_hierarchy():
    categories = Category.objects.all()
    category_dict = {}

    for category in categories:
        if category.parent is None:
            category_dict[category] = []

    for category in categories:
        if category.parent in category_dict:
            category_dict[category.parent].append(category)

    return category_dict

def category_hierarchy(request):
    return {
        'category_hierarchy': get_category_hierarchy()
    } 
def tags(request):
    return {
        'all_tags': Tag.objects.all().order_by('-id')[:10]
    }

def categories_with_counts(request):
    categories = Category.objects.filter(parent__isnull=True).annotate(post_count=Count('post')).order_by('-post_count')
    return {
        'footer_categories': categories
    } 
    
def Newslatter(request):  
    context = {}
    if request.method == 'POST':
        form = NewslatterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to the newsletter.')
        else:
            context['newsletter_form'] = form
            context['newsletter_form_errors'] = form.errors
    else:
        context['newsletter_form'] = NewslatterForm() 
    
    return context 



def category_hierarchy_header(request):
    hierarchy = {}
    categories = Category.objects.filter(parent__isnull=True)  

    for category in categories:
        posts = Post.objects.filter(category=category)
        
        # Fetch posts for child categories
        child_categories = Category.objects.filter(parent=category)
        for child in child_categories:
            child_posts = Post.objects.filter(category=child)
            posts = posts | child_posts  
        
        posts = posts[:3]

        hierarchy[category] = posts 
    return {'category_hierarchy_header': hierarchy} 

def popular_posts(request):
    popular_posts = Post.objects.order_by('-post_view')[:3]
    return {
        'popular_posts': popular_posts
    }
