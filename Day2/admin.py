from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Todo, Comment


@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    # List 조회시 title 앞에 username이 뜨도록
    list_display = ['get_title_with_username', 'user', 'is_completed', 'created_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'start_date', 'end_date')
        }),
        ('완료 정보', {
            'fields': ('is_completed', 'completed_image', 'thumbnail')
        }),
    )

    def get_title_with_username(self, obj):
        return f'{obj.user.username} - {obj.title}'

    get_title_with_username.short_description = 'Title'

    # admin이 모든 유저의 Todo 조회,수정,삭제 가능하게
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # admin은 모든 Todo 조회 가능
        return queryset.filter(user=request.user)

    @admin.register(Comment)
    class CommentAdmin(admin.ModelAdmin):
        list_display = ['id', 'user', 'todo', 'message', 'created_at']