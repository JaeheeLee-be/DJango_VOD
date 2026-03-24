from django import forms
from django_summernote.widgets import SummernoteWidget

from blog.models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('category', 'title', 'image','content', ) # __all__ : 전체 적용, 하는 경우가 아닌 떄는 list or tuple로 사용
        widgets = {
            'content': SummernoteWidget()
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'content': '댓글'
        }