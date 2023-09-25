


from django.core import paginator
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from blog.forms import EmailSendForm
from django.template import RequestContext

from blogproject import settings
from blog.forms import CommentForm
from taggit.models import Tag
from django.views.generic import ListView


# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all() # get all posts
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)  #Tag is model name inside taggit module (it is inbuilt module)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,3) # 3 posts per page
    page_number=request.GET.get('page') # current page
    try:
        post_list=paginator.page(page_number) #provide list of posts based on page number
    except PageNotAnInteger:  #when we are not sending page num along with request.
        post_list=paginator.page(1) #in this case it displays first page
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})  # value of dict is object

#if we want to execute using class based view
# class PostListView(ListView):
#     model=Post
#     paginate_by = 1


def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)   # related to comments
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)  #create form object
        if form.is_valid():
            new_comment=form.save(commit=False) #get the comment but dont save in DB
            new_comment.post=post  #pls associate the comment to the post. '=post' is from line 35
            new_comment.save()  #save in DB
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})
    # get_object_or_404 used for getting an object from a database using a model’s manager and raising an Http404 exception if the object is not found.

def mail_send_view(request, id, data=None):
    post=get_object_or_404(Post,id=id,status='published') #based on this id pls provide post object/post. 'Post' is model here
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data  #to get the data.End user provided data is always present in this dictionary

            subject='{} recommends you to read "{}"'.format(cd['name'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())  #this builds complete url
            message='Read post at:\n {}\n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'krish.karjagi1@gmail.com',[cd['to']])

            sent=True
    else:
        form=EmailSendForm()  #object or create a form
    return render(request,'blog/sharebyemail.html',{'form':form,'post':post,'sent':sent})
