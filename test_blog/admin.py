from django.contrib import admin

from test_blog.models import Blog, Post

admin.site.register(Blog)
admin.site.register(Post)