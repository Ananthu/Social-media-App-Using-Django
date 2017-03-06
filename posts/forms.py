from django import forms
from django.contrib.auth.models import User
from .models import Post,Comment,User_Detailed_Info

class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=["title","image","content"]


class RegistrationForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model=User
		fields=['username','email','password']

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField( widget = forms.PasswordInput)

	class Meta:
		model=User
		fields=['username','password']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text',]

class DetailedUserForm(forms.ModelForm):
	email=forms.CharField(widget=forms.EmailInput)

	class Meta:
		model=User_Detailed_Info
		fields = [ 'email','profile_pic','phone_no','about',]

