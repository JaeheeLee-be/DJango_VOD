from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

admin.site.register(Comment)


class CommentInline(admin.TabularInline): # admin page에서 댓글 목록 생성
    model = Comment
    fields = ['content', 'author']
    extra = 1 # 댓글 목록을 1개로 바꿔줌, 일반적인 댓글창으로 바꾼다고 생각하면 됌

@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ['content']
    inlines = [
        CommentInline,
    ]