from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^blog/$', 'test_blog.views.blog', name='my-blog'),
    url(r'^blog/(?P<blog>\d+)/$', 'test_blog.views.blog', name='blog'),
    url(r'^blog/(?P<blog>\d+)/subscribe/$', 'test_blog.views.blog_subscribe', {'subscribe': True}, name='blog-subscribe'),
    url(r'^blog/(?P<blog>\d+)/unsubscribe/$', 'test_blog.views.blog_subscribe', {'subscribe': False}, name='blog-unsubscribe'),
    url(r'^$', 'test_blog.views.blogs', name='blogs'),
    url(r'^post/(?P<post>\d+)/$', 'test_blog.views.post', name='post'),
    url(r'^post/(?P<post>\d+)/read/$', 'test_blog.views.post_read', name='post-read'),
    url(r'^post/(?P<post>\d+)/edit/$', 'test_blog.views.post', {'edit': True}, name='post-edit'),
    url(r'^post/add/$', 'test_blog.views.post', {'edit': True}, name='post-add'),
    url(r'^newsfeed/$', 'test_blog.views.newsfeed', name='newsfeed'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='auth')),
)
