# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME

from test_blog.models import Blog, Post
from test_blog.forms import PostForm

# Create your views here.


class BlogView(TemplateView):
    template_name = 'blog.html'

    def get(self, request, blog=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if blog is not None:
            blog = get_object_or_404(Blog, pk=blog)
        elif request.user.is_authenticated():
            try:
                blog = request.user.blog
            except AttributeError:
                return redirect('blogs')
        else:
            return redirect('blogs')
        context['blog'] = blog
        context['next'] = request.path
        return self.render_to_response(context)


class BlogsView(TemplateView):
    template_name = 'blogs.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        blogs = Blog.objects.all()
        context['blogs'] = blogs
        context['next'] = request.path
        return self.render_to_response(context)


class PostView(TemplateView):

    def get(self, request, post=None, edit=False, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['next'] = request.path
        if not post and not edit:
            raise Http404
        elif post:
            context['post'] = Post.objects.get(id=post)
        self.template_name = 'post/post.html'
        if edit:
            if (not request.user.is_authenticated()
            or (post and post.blog.user != request.user)):
                return redirect('post', post=post)
            self.template_name = 'post/edit.html'
            context['form'] = PostForm(instance=post)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, post=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if post:
            context['post'] = post = Post.objects.get(id=post)
            if post.blog.user != request.user:
                raise HttpResponseForbidden
        context['form'] = form = PostForm(request.POST,
                                          instance=post,
                                          initial={'blog': request.user.blog})

        if form.is_valid():
            post = form.save(commit=False)
            post.blog = request.user.blog
            post.save()
            return redirect('post', post=post.id)
        self.template_name = 'post/edit.html'
        return self.render_to_response(context)


class BlogSubscribeView(View):

    def get(self, request, blog, subscribe, *args, **kwargs):
        next = request.GET.get(REDIRECT_FIELD_NAME)
        blog = get_object_or_404(Blog, pk=blog)
        if subscribe:
            blog.subscribers.add(request.user)
        else:
            blog.subscribers.remove(request.user)
            posts = request.user.readed.filter(blog=blog)
            request.user.readed.remove(posts)
        return HttpResponseRedirect(next)


class NewsFeedView(TemplateView):
    template_name = 'newsfeed.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('blogs')
        context = self.get_context_data(**kwargs)
        blogs = request.user.blog_subscriptions.values_list('id')
        posts = Post.objects.filter(Q(blog__in=blogs) | Q(blog=request.user.blog))
        context['posts'] = posts
        context['next'] = request.path
        return self.render_to_response(context)


class PostReadView(View):

    def get(self, request, post, *args, **kwargs):
        next = request.GET.get(REDIRECT_FIELD_NAME)
        post = get_object_or_404(Post, pk=post)
        request.user.readed.add(post)
        return HttpResponseRedirect(next)


blog = BlogView.as_view()
blogs = BlogsView.as_view()
post = PostView.as_view()
newsfeed = NewsFeedView.as_view()
blog_subscribe = BlogSubscribeView.as_view()
post_read = PostReadView.as_view()