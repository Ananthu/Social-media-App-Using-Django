from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^(?P<id>\d+)/$',views.detail,name="detail"),

    #urls for the navigation bar
    url(r'^register/$',views.RegistrationView.as_view(), name='registration'),
    url(r'^login/$',views.LoginView.as_view(), name='login'),
	url(r'^logout$',views.logout_view,name="logout"),
	url(r'^add/$', views.PostCreate.as_view(), name='addpost'),

	#like-button
	url(r'^like_category/$', views.like_category, name='like_category'),

    url(r'^unlike_category/$', views.unlike_category, name='unlike_category'),

    url(r'^posts/(?P<id>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),

    #url to the detailed user information
    url(r'^user_info/$', views.user_info, name='user_info'),

    url(r'^user_info/edit/$', views.ProfileInfoUpdate, name='user_info_edit'),
    
    url(r'^create_post/$', views.post_create, name='create_post'),
    url(r'^post_update/(?P<id>\d+)/$', views.post_update, name='edit_post'),
    url(r'^post_delete/(?P<id>\d+)/$', views.post_delete, name='delete_post'),



]

