from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','body','publish','created','updated','status']
    list_filter = ('status','author','publish')  #  mentioned in the form of tuples usually
    search_fields = ('title','body')
    raw_id_fields = ('author',)     # we can get user based on id.Need to mention id
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    prepopulated_fields = {'slug':('title',)}
    # whatever we mention in title it reflects in slugfield

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','body','created','updated','active']
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)

