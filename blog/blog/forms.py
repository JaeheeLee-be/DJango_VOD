from django import forms
from blog.models import Blog



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content') # __all__ : 전체 적용, 하는 경우가 아닌 떄는 list or tuple로 사용
