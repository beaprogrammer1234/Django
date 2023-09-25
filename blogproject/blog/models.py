from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

# Create your models here.



class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.DO_NOTHING)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()  #this says, dont open default manager , open custom manager
    #IMPORTANT: we need to remember that there is implicit field called 'id'
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)   # latest posts must be on top. This is single value tuple hence needs ','

    #if anywhere i am going to publish this post object, internally str method is called and title is displayed
    def __str__(self):
        return self.title
    #now makemigrations,migrate and then register in admin,then create super user and then restart server

    def get_absolute_url(self): #this method tells Django how to calculate canonical URL
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
        # post_detail is defined in urls.py
        # reverse allows retrieving url details from urls.py file through name value provided

    #models related to comments section
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=32)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('created',)  #old to recent comments

    def __str__(self):  #if any person trying to display comments
        return 'commented by {} on {}'.format(self.name,self.post)