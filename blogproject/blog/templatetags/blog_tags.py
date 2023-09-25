from blog.models import Post
from django.db.models import Count
from django import template  # for below function to be template tag we need import and register the library
register=template.Library()  #object created

@register.simple_tag      #registering function as template tag. Simple tag returns value.
def total_posts():
    return Post.objects.count()    #'Post' is model


@register.inclusion_tag('blog/latest_posts123.html')  #Response of inclusion template tag is included in latest_posts123.html
def show_latest_posts(count=4):
    latest_posts=Post.objects.order_by('-publish')[:count]   #new to old posts and only top 3
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts():
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')
#pls count the comments from all posts and assign it to variable 'total_comments'
