from django import forms
from blog.models import Comment

class EmailSendForm(forms.Form):  # normal form
    name=forms.CharField()
    # email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)  #comments are optional so required=False

class CommentForm(forms.ModelForm):    # model based form
    class Meta:
        model=Comment
        fields=('name','body')

