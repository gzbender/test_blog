# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    name = models.CharField('Name', max_length=255, blank=True)
    user = models.OneToOneField(User)
    subscribers = models.ManyToManyField(User, related_name='blog_subscriptions')
    #posts - all blog posts

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('Title', max_length=255)
    content = models.TextField('Content', blank=True)
    created = models.DateTimeField('Created', auto_now=True, auto_now_add=True)
    blog = models.ForeignKey(Blog, related_name='posts')
    readers = models.ManyToManyField(User, related_name='readed')

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u'%s-%s, %s' % (self.blog.name, self.title, self.created)


def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance, name='Blog %s' % instance.username)


models.signals.post_save.connect(create_blog, sender=User)