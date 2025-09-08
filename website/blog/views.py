from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import connections

from .models import Blog, User, Comment

def index(request):
    blogs = Blog.objects.order_by('-pub_date')[:5]
    if request.user.is_authenticated:
        logged_in = True
        user = request.user
    else:
        logged_in = False
        user = False
    context = { 'blogs': blogs, 'logged_in': logged_in, 'user': user }
    return render(request, 'blog/index.html', context)


def create_new_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            new_user = User.objects.create_user(username=username, password=password1)
            new_user.save()
            login(request, new_user)
            return redirect('/blog')
        else:
            context = { 'error': True }
            return render(request, 'blog/user_creation.html', context)
    
    context = { 'error': False }
    return render(request, 'blog/user_creation.html', context)


"""
FIX 1

def create_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/blog')
    else:
        form = UserCreationForm()
    
    context = { 'form': form }
    return render(request, 'blog/user_creation.html', context) 

"""

def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog)
    comments = [ comment.text for comment in comments ]
    logged_in = request.user.is_authenticated
    user = blog.user
    context = { 'blog': blog, 'logged_in': logged_in, 'comments':comments, 'user': user }
    return render(request, 'blog/blog_page.html', context)
 

def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=user)
    blogs = [{ 'id': blog.id, 'title': blog.title, 'text': blog.text, 'likes': blog.likes, 'pub_date': blog.pub_date } for blog in blogs]
    context = { 'user': user, 'blogs': blogs }
    return render(request, 'blog/user_page.html', context)

    
"""
FIX 2


def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    is_user = False
    if request.user.is_authenticated:
        if request.user == user:
            is_user = True
    
    blogs = Blog.objects.filter(user=user)
    blogs = [{ 'id': blog.id, 'title': blog.title, 'text': blog.text, 'likes': blog.likes, 'pub_date': blog.pub_date } for blog in blogs]
    context = { 'user': user, 'blogs': blogs, 'is_user': is_user }
    return render(request, 'blog/user_page.html', context)
"""

        
#@login_required
def blog_form(request):
    context = { 'user_id': request.user.id }
    return render(request, 'blog/blog_form.html', context)

#@login_required
def create_blog(request):
    user = request.user
    ## FIX 4 change GET to POST
    # title = request.POST['title']
    #text = request.POST['text']

    title = request.GET['title']
    text = request.GET['text']
    pub_date = timezone.now()
    
    new_blog = Blog(user=user, title=title, text=text, pub_date=pub_date)
    new_blog.save()
    return redirect('/blog')


"""
FIX 3

@login_required
def create_comment(request, blog_id):
    user = request.user
    text = request.POST['new_comment']
    blog = Blog.objects.get(id=blog_id)

    new_comment = Comment(user=user, blog=blog, text=text)
    new_comment.save()

    return redirect('/blog/'+str(blog_id)+'/')

"""

def create_comment(request, blog_id):
    user = request.user
    text = request.GET['new_comment']
    blog = Blog.objects.get(id=blog_id)

    # use this comment for sql injection test: '); DELETE FROM blog_comment; --

    with connections['default'].cursor() as c:
        c.executescript("INSERT INTO blog_comment (user_id, blog_id, text) VALUES ('"+str(user.id)+"', '"+str(blog.id)+"', '"+text+"');")
    
    return redirect('/blog/'+str(blog_id)+'/')
    

def delete_blog(request, blog_id):
    user_id = request.user.id
    blog = Blog.objects.get(id=blog_id)
    blog.delete()

    return redirect('/blog/user/'+str(user_id))

"""
FIX 2

#@login_required
def delete_blog(request, blog_id):
    user_id = request.user.id
    blog = Blog.objects.get(id=blog_id)
    if request.user == blog.user:
        blog.delete()

    return redirect('/blog/user/'+str(user_id))

"""