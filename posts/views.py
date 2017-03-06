from django.http import HttpResponse 
from django.shortcuts import render,get_object_or_404,redirect
from django.core.urlresolvers import reverse
from models import Post,Comment,User_Detailed_Info
from forms import PostForm,CommentForm,DetailedUserForm
from django.views.generic import View
from forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# Create your views here.
def post_create(request):
	form=PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.created_user=request.user
		instance.save()
	context={ "form":form }
	return render(request,"my_blog/post_create.html",context)

def post_update(request,id=None):
	instance=get_object_or_404(Post,id=id)
	if instance.created_user != request.user.username :
		messages.success(request, "Post owned by another user, You are having read permission only")
		return render(request,"my_blog/denied.html",{})
	else :	
		form=PostForm(request.POST or None,request.FILES or None,instance=instance)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
		context={ "form":form,
				  "instance":instance }

		return render(request,"my_blog/post_create.html",context)

def post_delete(request,id):
	form=PostForm(request.POST or None)
	instance=get_object_or_404(Post,id=id)
	if instance.created_user != request.user.username :
		messages.success(request, "Post owned by another user, You are having read permission only")
		return render(request,"my_blog/denied.html",{})

	else:
		instance.delete()
		return redirect("posts:index")

def index(request):
	lists=Post.objects.all().order_by("-timestamp")
	return render(request,"my_blog/index.html",{'lists':lists})


def detail(request,id):
	lists=Post.objects.get(pk=id)
	return render(request,"my_blog/detail.html",{'lists':lists,})



class RegistrationView(View):
	form_class=RegistrationForm
	template_name='my_blog/user_login_form.html'


	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=self.form_class(request.POST)

		if form.is_valid():

			user=form.save(commit=False)

			#cleaned (normalized) data
			username =form.cleaned_data['username']
			password =form.cleaned_data['password']
			email=form.cleaned_data['email']
			user.set_password(password)
			user.save()

			#saving the basic data to another model for user datails
			temp_user_details=User_Detailed_Info()
			temp_user_details.name=username
			temp_user_details.email=email
			temp_user_details.save()

			messages.success(request,"User successfully created now logIn please")
		return render(request,self.template_name,{'form':form,})


class LoginView(View):
	form_class=LoginForm
	template_name='my_blog/user_login_form.html'


	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=self.form_class(request.POST)

		if form.is_valid():


			#cleaned (normalized) data
			username =form.cleaned_data['username']
			password =form.cleaned_data['password']

	

			#authentication

			user=authenticate(username=username,password=password)

			if user:
				pass
			else:
				messages.success(request,"Wrong password or username")
				

			if user is not None:
				if user.is_active:
						login(request,user)
						lists=Post.objects.all().order_by("-timestamp")
						return render(request,'my_blog/index.html',{"user":user,"lists":lists})

		return render(request,self.template_name,{'form':form})


#-----log-out

def logout_view(request):
    logout(request)
    return redirect('posts:index')


# for creating new posts

class PostCreate(CreateView):
	model=Post
	template_name='my_blog/post_form.html'
	fields=['title','image','content']


# likes for the post
def like_category(request):

    post_id = None
    if request.method == 'GET':
        post_id = request.GET['like_id']

    likes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            likes = post.likes + 1
            post.likes =  likes
            post.save()

    return HttpResponse(likes)

def unlike_category(request):

    post_id = None
    if request.method == 'GET':
        post_id = request.GET['dislike_id']

    unlikes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            unlikes = post.dislikes + 1
            post.dislikes =  unlikes
            post.save()

    return HttpResponse(unlikes)



def add_comment_to_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author=request.user
            comment.save()
            return redirect('posts:detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'my_blog/add_comment_to_post.html', {'form': form})

#to see the detailed user information

def user_info(request):
	print request.user
	current_user=User_Detailed_Info.objects.get(name=request.user)
	user_posts=Post.objects.filter(created_user=request.user.username)
	return render(request,'my_blog/user_detailed_info.html',{"current_user":current_user,"user_posts":user_posts})


def ProfileInfoUpdate(request):
	instance=User_Detailed_Info.objects.get(name=request.user)
	form=DetailedUserForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
	context={ "form":form,
			  "instance":instance }

	return render(request,"my_blog/post_create.html",context)

