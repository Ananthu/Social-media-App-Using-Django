from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.shortcuts import redirect
# Create your models here.


class Post(models.Model):
	title=models.CharField(max_length=120)
	image=models.FileField(null=True,blank=True)
	content=models.TextField()
	updated=models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
	likes=models.IntegerField(default=0)
	dislikes=models.IntegerField(default=0)
	created_user=models.CharField(max_length=120,blank=True)

	def get_absolute_url(self):
		return reverse('posts:detail',kwargs={'id':self.id})


	def __str__(self):
		return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class User_Detailed_Info(models.Model):
	name=models.CharField(max_length=120)
	email = models.EmailField(max_length=70,blank=True)
	phone_no=models.IntegerField(default=0,blank=True)
	about=models.TextField(blank=True)
	profile_pic=models.FileField(blank=True)



	def __str__(self):
		return self.name