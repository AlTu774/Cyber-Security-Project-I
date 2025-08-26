from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Blog, User, Comment

def index(request):
    blogs = Blog.objects.order_by('-pub_date')[:3]
    if request.user.is_authenticated:
        logged_in = True
        user = request.user
    else:
        logged_in = False
        user = False
    context = { 'blogs': blogs, 'logged_in': logged_in, 'user': user }
    return render(request, 'blog/index.html', context)

def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog)
    comments = [ comment.text for comment in comments ]
    logged_in = request.user.is_authenticated
    context = { 'blog': blog, 'logged_in': logged_in, 'comments':comments }
    return render(request, 'blog/blog_page.html', context)

def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=user)
    blogs = [{ 'id': blog.id, 'title': blog.title, 'text': blog.text, 'likes': blog.likes, 'pub_date': blog.pub_date } for blog in blogs]
    context = { 'user': user, 'blogs': blogs }
    return render(request, 'blog/user_page.html', context)

def blog_form(request):
    context = { 'user_id': request.user.id }
    return render(request, 'blog/blog_form.html', context)

def create_blog(request):
    #user = User.objects.get(id=request.user.id)
    user = request.user
    title = request.GET['title']
    text = request.GET['text']
    pub_date = timezone.now()
    
    new_blog = Blog(user=user, title=title, text=text, pub_date=pub_date)
    new_blog.save()
    return redirect('/blog')

def create_comment(request, blog_id):
    user = request.user
    text = request.GET['new_comment']
    blog = Blog.objects.get(id=blog_id)

    new_comment = Comment(user=user, blog=blog, text=text)
    new_comment.save()
    return redirect('/blog/'+str(blog_id)+'/')

def delete_blog(request, blog_id):
    user_id = request.user.id
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('/blog/user/'+str(user_id))