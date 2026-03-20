from django.urls import path
from . import views, cb_views

urlpatterns = [
    # FBV
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/', views.todo_info, name='todo_info'),
    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),

    # CBV
    path('todo/', cb_views.TodoListView.as_view(), name='cbv_todo_list'),
    path('todo/create/', cb_views.TodoCreateView.as_view(), name='cbv_todo_create'),
    path('todo/<int:pk>/', cb_views.TodoDetailView.as_view(), name='cbv_todo_info'),
    path('todo/<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('todo/<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='cbv_todo_delete'),
]