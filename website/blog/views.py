from django.shortcuts import render
from django.http import HttpResponse

from .models import Blog

def index(request):
    blogs = Blog.objects.order_by('-pub_date')[:3]
    context = { 'blogs': blogs }
    return render(request, 'blog/index.html', context)

def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    context = { 'blog': blog }
    return render(request, 'blog/blog_page.html', context)