from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=15, default='Untitled')
  text = models.CharField(max_length=2000)
  likes = models.IntegerField(default=0)
  pub_date = models.DateField()

class Comment(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
  text = models.CharField(max_length=150)

