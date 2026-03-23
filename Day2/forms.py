from django import forms
from .models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date']


class TodoUpdateForm(TodoForm):
    class Meta(TodoForm.Meta):
        fields = TodoForm.Meta.fields + ['is_completed']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message': '내용'
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'class': 'form-control',
                'placeholder': '댓글을 입력하세요.'
            })
        }