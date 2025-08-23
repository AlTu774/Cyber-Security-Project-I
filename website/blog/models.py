from django.db import models

class Blog(models.Model):
  title = models.CharField(max_length=15, default='Untitled')
  text = models.CharField(max_length=2000)
  likes = models.IntegerField(default=0)
  pub_date = models.DateField()

class Comment(models.Model):
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
  text = models.CharField(max_length=150)

