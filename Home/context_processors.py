from Home.models import Category 

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