from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blog_id>/', views.blog_view),
    path('user/<int:user_id>/', views.user_view),
    path('create_blog/', views.blog_form),
    path('confirm_blog/', views.create_blog),
    path('<int:blog_id>/create_comment/', views.create_comment),
    path('<int:blog_id>/delete/', views.delete_blog)
]