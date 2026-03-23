from django.urls import path
from . import cb_views

urlpatterns = [
    # CBV
    path('todo/', cb_views.TodoListView.as_view(), name='cbv_todo_list'),
    path('todo/create/', cb_views.TodoCreateView.as_view(), name='cbv_todo_create'),
    path('todo/<int:pk>/', cb_views.TodoDetailView.as_view(), name='cbv_todo_info'),
    path('todo/<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('todo/<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='cbv_todo_delete'),
]