from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # List 조회시 title 앞에 username이 뜨도록
    list_display = ['get_title_with_username', 'user', 'is_completed', 'created_at']

    def get_title_with_username(self, obj):
        return f'{obj.user.username} - {obj.title}'
    
    get_title_with_username.short_description = 'Title'

    # admin이 모든 유저의 Todo 조회,수정,삭제 가능하게
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # admin은 모든 Todo 조회 가능
        return queryset.filter(user=request.user)