from django.contrib import admin
from models import Post,Comment,User_Detailed_Info

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User_Detailed_Info)

