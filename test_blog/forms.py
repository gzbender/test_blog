# -*- coding: utf-8 -*-

from django.forms import ModelForm

from test_blog.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
