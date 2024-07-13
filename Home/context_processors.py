from Home.models import Category  
from taggit.models import Tag 
from django.db.models import Count

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