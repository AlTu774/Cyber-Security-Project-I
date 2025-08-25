from django.shortcuts import render
from django.http import HttpResponse

from .models import Blog, User

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
    context = { 'blog': blog }
    return render(request, 'blog/blog_page.html', context)

def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=user)
    blogs = [{ 'id':blog.id, 'title': blog.title, 'text': blog.text, 'likes': blog.likes, 'pub_date': blog.pub_date } for blog in blogs]
    print(user)
    context = { 'user': user, 'blogs': blogs }
    return render(request, 'blog/user_page.html', context)