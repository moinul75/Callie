from django.shortcuts import render,redirect ,get_object_or_404
from .models import Category,Post,PostImage,Comment,Reply
from django.contrib import messages
from .forms import NewslatterForm,CommentForm,ReplyForm
from django.utils import timezone
from datetime import timedelta 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from Account.models import User 

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
    # Handle newsletter subscription form
    if request.method == 'POST':
        form = NewslatterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to the newsletter.')
            return redirect('index')  # Redirect to avoid resubmission on refresh
        else:
            # Collect all form errors and display them
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
    else:
        form = NewslatterForm()
        
    # Fetch data for the homepage
    categories = Category.objects.all()
    recent_posts = Post.objects.order_by('-created_at')[:4]
    lifestyle_posts = Post.objects.filter(category__name='Life Style')
    
    # Create a dictionary of hero posts with the latest post per category
    hero_posts = {}
    for category in categories:
        latest_post = Post.objects.filter(category=category).order_by('-created_at').first()
        if latest_post:
            hero_posts[category] = latest_post

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
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Handling view count with session
    last_viewed_str = request.session.get(f'post_{post_id}_last_viewed')
    last_viewed = None
    if last_viewed_str:
        try:
            last_viewed = timezone.datetime.fromisoformat(last_viewed_str)
            if last_viewed.tzinfo is None:
                last_viewed = timezone.make_aware(last_viewed)
        except ValueError:
            last_viewed = None

    now = timezone.now()

    if last_viewed is None or (now - last_viewed) > timedelta(minutes=5):
        post.post_view += 1
        post.save()
        request.session[f'post_{post_id}_last_viewed'] = now.isoformat()

    # Handling comment submission
    if request.method == 'POST':
        # If not authenticated, handle registration
        if not request.user.is_authenticated:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(username=username).exists():
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                else:
                    messages.error(request, 'Authentication failed. Please try again.')
                    return redirect(post.get_absolute_url())
            else:
                messages.error(request, 'Username already exists.')
                return redirect(post.get_absolute_url())

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'There was a problem with your comment.')

    else:
        form = CommentForm()

    # Handling reply submission (separate form handling)
    if 'reply_content' in request.POST:
        reply_form = ReplyForm(request.POST)
        parent_comment_id = request.POST.get('parent_comment_id')
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = parent_comment
            reply.user = request.user
            reply.save()
            messages.success(request, 'Your reply has been added.')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'There was a problem with your reply.')
    else:
        reply_form = ReplyForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'reply_form': reply_form,
    }
    return render(request, 'details_blog.html', context)



@login_required
def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            messages.success(request, 'Your reply has been added.')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'There was a problem with your reply.')
    else:
        form = ReplyForm()
    return render(request, 'add_reply.html', {'form': form, 'post': post, 'comment': comment})

def blog(request): 
    return render(request,'blog-post.html')  

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'category.html', context)

def about(request): 
    return render(request,'about.html')   

def author(request): 
    return render(request, 'author.html')

